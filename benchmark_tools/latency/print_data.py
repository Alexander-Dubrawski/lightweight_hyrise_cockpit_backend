from statistics import mean, median


def print_green(value):
    """Print green colored text."""
    print("\033[92m{}\033[00m".format(value))


def print_cyan(value):
    """Print cyan colored text."""
    print("\033[96m{}\033[00m".format(value))


def print_data(endpoint, results):
    print_green(f"\nResults for {endpoint}")
    print_cyan("Server process time")
    print(f"Avg: {round(mean(results['server_process_times']) * 1_000, 4)}ms")
    print(f"Median: {round(median(results['server_process_times']) * 1_000, 4)}ms")
    print_cyan("Name lookup time")
    print(f"Avg: {round(mean(results['name_lookup_times']) * 1_000, 4)}ms")
    print(f"Median: {round(median(results['name_lookup_times']) * 1_000, 4)}ms")
    print_cyan("Connect time")
    print(f"Avg: {round(mean(results['connect_times']) * 1_000, 4)}ms")
    print(f"Median: {round(median(results['connect_times']) * 1_000,4)}ms\n")
