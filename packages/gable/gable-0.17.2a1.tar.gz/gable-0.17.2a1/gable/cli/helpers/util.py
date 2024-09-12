from typing import Generator, List


def chunk_list(
    input_list: List[str], chunk_size: int
) -> Generator[List[str], None, None]:
    """Splits a list into chunks of specified size."""
    for i in range(0, len(input_list), chunk_size):
        yield input_list[i : i + chunk_size]
