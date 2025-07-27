import sys
import math
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def load_data(filename: str) -> Dict[str, List[Tuple[float, float, float]]]:
    """
    Loads CSV data from a file and groups measurements by batch.
    
    Args:
        filename: Path to the CSV file.
    
    Returns:
        A dictionary where keys are batch numbers (str) and values are lists 
        of tuples (x, y, measurement).
    
    Raises:
        FileNotFoundError: If the file does not exist.
    """
    batch_data = {}
    try:
        with open(filename, 'r') as file:
            for line_number, line in enumerate(file, 1):
                line = line.strip()
                if not line:
                    continue  # Skip empty lines
                
                try:
                    parts = [part.strip() for part in line.split(',')]
                    if len(parts) != 4:
                        raise ValueError(f"Expected 4 values, got {len(parts)}")
                    
                    batch, x, y, val = parts
                    x, y, val = float(x), float(y), float(val)
                    
                    if batch not in batch_data:
                        batch_data[batch] = []
                    batch_data[batch].append((x, y, val))
                
                except ValueError as e:
                    print(f"Warning: invalid data in line {line_number}: {line} ({e})", file=sys.stderr)
    
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.", file=sys.stderr)
        sys.exit(1)
    
    return batch_data


def filter_within_unit_circle(samples: List[Tuple[float, float, float]]) -> List[Tuple[float, float, float]]:
    """
    Filters samples to only include points inside the unit circle (x² + y² ≤ 1).
    
    Args:
        samples: List of tuples (x, y, measurement).
    
    Returns:
        Filtered list of tuples.
    """
    return [(x, y, val) for (x, y, val) in samples if x**2 + y**2 <= 1]


def calculate_average(measurements: List[float]) -> float:
    """
    Calculates the average of measurement values.
    
    Args:
        measurements: List of measurement values.
    
    Returns:
        Average value, or 0 if the list is empty.
    """
    if not measurements:
        return 0.0
    return sum(measurements) / len(measurements)


def print_results(batch_averages: Dict[str, float]) -> None:
    """
    Prints batch averages in a sorted, formatted table.
    
    Args:
        batch_averages: Dictionary with batch numbers (str) as keys 
                        and average values (float) as values.
    """
    print("Batch\tAverage")
    for batch, avg in sorted(batch_averages.items(), key=lambda x: int(x[0])):
        print(f"{batch}\t{avg}")


def plot_data(data: Dict[str, List[Tuple[float, float, float]]], output_filename: str) -> None:
    """
    Plots all data points within and outside the unit circle, with batch-specific colors.
    
    Args:
        data: Dictionary with batch numbers as keys and lists of (x, y, value) tuples.
        output_filename: Base filename for the output plot (e.g., 'sample1' -> 'sample1.pdf').
    """
    plt.figure()
    
    # Draw unit circle
    angles = [n/150 * 2 * math.pi for n in range(151)]
    x_circle = [math.cos(a) for a in angles]
    y_circle = [math.sin(a) for a in angles]
    plt.plot(x_circle, y_circle, 'k-')  # 'k-' = black solid line
    
    # Plot each batch with a unique color
    colors = ['b', 'g', 'r', 'c', 'm', 'y']  # Supports up to 6 batches
    for i, (batch, samples) in enumerate(data.items()):
        color = colors[i % len(colors)]
        x_vals, y_vals, vals = zip(*samples) if samples else ([], [], [])
        plt.scatter(x_vals, y_vals, c=color, label=f'Batch {batch}')
        
        # Annotate each point with its value
        for x, y, val in samples:
            plt.text(x, y, f"{val:.1f}", fontsize=8, ha='center', va='bottom')
    
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Data Points by Batch')
    plt.legend()
    plt.grid(True)
    plt.axis('equal')  # Fix aspect ratio to avoid oval circle
    
    plt.savefig(f"{output_filename}.pdf")
    print(f"A plot of the data can be found in {output_filename}.pdf")


def main() -> None:
    """
    Main function: Orchestrates data loading, processing, output, and plotting.
    """
    filename = input('Which CSV file should be analyzed? ').strip()
    batch_data = load_data(filename)
    
    # Calculate batch averages (filtered to unit circle)
    batch_averages = {}
    for batch, samples in batch_data.items():
        filtered_samples = filter_within_unit_circle(samples)
        measurements = [val for (_, _, val) in filtered_samples]
        batch_averages[batch] = calculate_average(measurements)
    
    print_results(batch_averages)
    plot_data(batch_data, filename.replace('.csv', ''))


if __name__ == '__main__':
    main()