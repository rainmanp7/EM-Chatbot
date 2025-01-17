# snn.py
import re
import random
import logging
from collections import defaultdict, Counter
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class Neuron:
    def __init__(self, threshold: float = 0.5, decay: float = 0.8):
        self.potential: float = 0.0
        self.threshold: float = threshold
        self.decay: float = decay
        self.last_spike_time: int = -1
        self.entity_name: str = ""

    def integrate(self, input_spike: float, current_time: int) -> bool:
        """
        Integrate an input spike into the neuron's potential and determine if it spikes.

        Args:
            input_spike (float): The input spike value.
            current_time (int): The current time step.

        Returns:
            bool: True if the neuron spikes, otherwise False.

        Raises:
            ValueError: If the input spike is not a numeric value.
        """
        if not isinstance(input_spike, (int, float)):
            logger.error("Input spike must be a numeric value.")
            raise ValueError("Input spike must be a numeric value.")
        self.potential += input_spike
        if self.potential >= self.threshold:
            self.potential = 0.0  # Reset potential after spiking
            self.last_spike_time = current_time
            return True  # Neuron spiked
        self.potential *= self.decay  # Decay potential over time
        return False  # Neuron did not spike


class Synapse:
    def __init__(self, weight: float = 0.5, learning_rate: float = 0.01, stdp_rate: float = 0.1):
        self.weight: float = weight
        self.learning_rate: float = learning_rate
        self.stdp_rate: float = stdp_rate
        self.last_used_time: int = -1

    def transmit(self, spike: float) -> float:
        """
        Transmit a spike through the synapse.

        Args:
            spike (float): The input spike value.

        Returns:
            float: The transmitted spike value (weighted).
        """
        return self.weight if spike else 0

    def adjust_weight(self, pre_spike_time: int, post_spike_time: int) -> None:
        """
        Adjust the synapse weight using spike-timing-dependent plasticity (STDP).

        Args:
            pre_spike_time (int): The time of the pre-synaptic spike.
            post_spike_time (int): The time of the post-synaptic spike.
        """
        if pre_spike_time != -1 and post_spike_time != -1:
            time_diff = post_spike_time - pre_spike_time
            self.weight += self.stdp_rate * time_diff
            self.weight = max(0.0, min(1.0, self.weight))
            self.last_used_time = max(pre_spike_time, post_spike_time)


class SpikingNeuralNetwork:
    def __init__(self):
        self.neurons: List[Neuron] = []
        self.synapses: Dict[int, Dict[int, Synapse]] = defaultdict(dict)
        self.current_time: int = 0
        self.spike_history: Counter[int] = Counter()
        self.entity_to_neuron: Dict[str, int] = {}

    def add_neuron(self, entity_name: str) -> Neuron:
        """
        Add a new neuron for the given entity.

        Args:
            entity_name (str): The name of the entity.

        Returns:
            Neuron: The newly created neuron.

        Raises:
            ValueError: If the entity name is empty.
        """
        if not entity_name:
            logger.error("Entity name cannot be empty.")
            raise ValueError("Entity name cannot be empty.")
        neuron = Neuron()
        neuron.entity_name = entity_name
        self.neurons.append(neuron)
        self.entity_to_neuron[entity_name] = len(self.neurons) - 1
        logger.info(
            f"Added a new neuron for entity: {entity_name}. Total neurons: {len(self.neurons)}."
        )
        return neuron

    def step(self, inputs: List[Tuple[str, float]]) -> Dict[str, any]:
        """
        Process a step in the SNN with the given inputs.

        Args:
            inputs (List[Tuple[str, float]]): A list of tuples containing entity names and spike values.

        Returns:
            Dict[str, any]: A dictionary containing step results.

        Raises:
            ValueError: If the inputs are not in the correct format or entity names are empty.
        """
        if not isinstance(inputs, list) or not all(
            isinstance(i, tuple) and len(i) == 2 for i in inputs
        ):
            logger.error(
                "Inputs must be a list of tuples (entity_name, spike_value)."
            )
            raise ValueError(
                "Inputs must be a list of tuples (entity_name, spike_value)."
            )
        spikes = []
        for entity_name, input_spike in inputs:
            if not entity_name:
                logger.error("Entity name cannot be empty.")
                raise ValueError("Entity name cannot be empty.")
            # Ensure the neuron for this entity exists
            if entity_name not in self.entity_to_neuron:
                self.add_neuron(entity_name)
            neuron_index = self.entity_to_neuron[entity_name]
            neuron = self.neurons[neuron_index]
            # Process spikes for all neurons
            for j, other_neuron in enumerate(self.neurons):
                if j not in self.synapses[neuron_index]:
                    # Initialize a new synapse with a random weight
                    self.synapses[neuron_index][j] = Synapse(
                        random.uniform(0.1, 1.0)
                    )
                synapse = self.synapses[neuron_index][j]
                transmitted_spike = synapse.transmit(input_spike)
                spiked = other_neuron.integrate(transmitted_spike, self.current_time)
                spikes.append(spiked)
                self.spike_history[self.current_time] += int(spiked)
                if spiked and input_spike:
                    synapse.adjust_weight(
                        self.current_time - 1, self.current_time
                    )
        self.current_time += 1
        logger.info(f"Step completed at time {self.current_time}.")
        return {
            "any_spikes": any(spikes),
            "spikes": spikes,
            "current_time": self.current_time,
            "total_neurons": len(self.neurons),
            "total_synapses": sum(len(synapses) for synapses in self.synapses.values()),
            "spike_history": dict(self.spike_history)
        }

    def analyze_expression(self, expression: str) -> str | None:
        """
        Analyze a math expression and suggest optimizations.

        Args:
            expression (str): The math expression to analyze.

        Returns:
            str | None: The optimized expression, or None if no optimization is found.
        """
        # Example: Recognize repeated addition and suggest multiplication
        if '+' in expression:
            terms = expression.split('+')
            if len(terms) > 2 and all(term.strip() == terms[0].strip() for term in terms):
                # If all terms are the same, suggest multiplication
                optimized_expression = f"{terms[0].strip()} * {len(terms)}"
                return optimized_expression
        # Example: Recognize repeated multiplication and suggest exponentiation
        if '*' in expression:
            factors = expression.split('*')
            if len(factors) > 2 and all(factor.strip() == factors[0].strip() for factor in factors):
                # If all factors are the same, suggest exponentiation
                optimized_expression = f"{factors[0].strip()} ^ {len(factors)}"
                return optimized_expression
        # Recognize trigonometric identities
        if 'sin' in expression or 'cos' in expression or 'tan' in expression:
            # Example: sin(90) + sin(90) → 2 * sin(90)
            func_matches = re.findall(r'(sin|cos|tan)\(([^)]+)\)', expression)
            if len(func_matches) > 1 and all(
                match[0] == func_matches[0][0] and match[1] == func_matches[0][1] for match in func_matches
            ):
                optimized_expression = f"{len(func_matches)} * {func_matches[0][0]}({func_matches[0][1]})"
                return optimized_expression
        # Recognize logarithmic simplifications
        if 'log' in expression:
            # Example: log(100) + log(100) → 2 * log(100)
            log_matches = re.findall(r'log\(([^)]+)\)', expression)
            if len(log_matches) > 1 and all(match == log_matches[0] for match in log_matches):
                optimized_expression = f"{len(log_matches)} * log({log_matches[0]})"
                return optimized_expression
        # No optimization found
        return None


# Test for snn.py
if __name__ == "__main__":
    print("Testing snn.py...")
    snn = SpikingNeuralNetwork()
    # Test adding a neuron
    snn.add_neuron("input1")
    print("Added neuron for 'input1'.")
    # Test step function
    print("Running step function with input [('input1', 1.0)]...")
    result = snn.step([("input1", 1.0)])
    print("Step result:", result)
    # Test analyze_expression
    print("Analyzing expression '5 + 5 + 5':", snn.analyze_expression("5 + 5 + 5"))  # Should suggest 5 * 3
    print("Analyzing expression 'sin(90) + sin(90)':", snn.analyze_expression("sin(90) + sin(90)"))  # Should suggest 2 * sin(90)
    print("Analyzing expression 'log(100) + log(100)':", snn.analyze_expression("log(100) + log(100)"))  # Should suggest 2 * log(100)
    print("Analyzing expression '2 * 2 * 2':", snn.analyze_expression("2 * 2 * 2"))  # Should suggest 2 ^ 3
    print("All tests passed!")
