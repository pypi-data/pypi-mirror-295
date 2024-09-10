"""Extract subchunks from PDF file."""

import operator
from functools import reduce
from pathlib import Path
from typing import Any

import pymupdf

from unichunking.types import ChunkPosition, SubChunk


def _handle_line(
    line: Any,
    dimensions: tuple[float, float],
    subchunk_idx: int,
    page_num: int,
    file_name: str,
) -> tuple[list[SubChunk], int]:
    line_chunks: list[SubChunk] = []
    for span in line["spans"]:
        text = str(span["text"].replace("�", " ").strip())
        font: Any = span["font"]
        bbox: Any = span["bbox"]
        if "bold" in font.lower():
            text = f"**{text}**"
        if text:
            x0, y0, x1, y1 = bbox
            width, height = dimensions
            position = ChunkPosition(
                x0=x0 / width,
                y0=y0 / height,
                x1=x1 / width,
                y1=y1 / height,
            )
            line_chunks.append(
                SubChunk(
                    subchunk_id=subchunk_idx,
                    content=text,
                    page=page_num,
                    position=position,
                    file_name=file_name,
                ),
            )
            subchunk_idx += 1

    return line_chunks, subchunk_idx


async def _retrieve_subchunks(
    path: Path,
    status_manager: Any,
) -> list[list[list[list[SubChunk]]]]:
    chunks: list[list[list[list[SubChunk]]]] = []
    idx = 0

    with pymupdf.Document(path) as doc:
        num_pages: Any = doc.page_count  # type: ignore
        for page_num in range(num_pages):
            if page_num % int(num_pages / 17 + 1) == 0:
                page_progress = int((page_num + 1) / num_pages * 75)
                await status_manager.update_status(
                    progress=page_progress,
                    start=status_manager.start,
                    end=status_manager.end,
                )
            page_chunks: list[list[list[SubChunk]]] = []
            textpage: Any = doc.load_page(page_num).get_textpage()  # type: ignore
            page = textpage.extractDICT(sort=False)

            dimensions = page["width"], page["height"]
            blocks = page["blocks"]

            for block in blocks:
                block_chunks: list[list[SubChunk]] = []
                lines = block["lines"]
                for line in lines:
                    line_chunks, idx = _handle_line(
                        line=line,
                        dimensions=dimensions,
                        subchunk_idx=idx,
                        page_num=page_num,
                        file_name=path.name,
                    )
                    if line_chunks:
                        block_chunks.append(line_chunks)
                if block_chunks:
                    page_chunks.append(block_chunks)
            if page_chunks:
                chunks.append(page_chunks)

    return chunks


def _filter_subchunks(
    chunks: list[list[list[list[SubChunk]]]],
) -> list[SubChunk]:
    flattened_chunks: list[SubChunk] = []

    for page_chunks in chunks:
        for block_chunks in page_chunks:
            for line_chunks in block_chunks:
                if line_chunks:
                    filtered_line_chunks = reduce(operator.add, line_chunks)
                    flattened_chunks.append(filtered_line_chunks)

    return flattened_chunks


async def extract_subchunks_pdf(
    path: Path,
    status_manager: Any,
) -> list[SubChunk]:
    """Filetype-specific function : extracts subchunks from a PDF file.

    Args:
        path: Path to the local file.
        status_manager: Optional, special object to manage task progress.

    Returns:
        A list of SubChunk objects.
    """
    chunks = await _retrieve_subchunks(
        path=path,
        status_manager=status_manager,
    )

    flattened_chunks = _filter_subchunks(chunks)

    progress = 100
    await status_manager.update_status(
        progress=progress,
        start=status_manager.start,
        end=status_manager.end,
    )

    return flattened_chunks
