from advanced_automation_utilities import Screen, ScreenInfo
import math

def check(is_text_present,final_text):
    rv = False
    if is_text_present in final_text:
        rv = True
    return rv

def get_text_from_monitor_screen(block_width, block_height, is_text_present):
    # Get the usable desktop area
    left, top, right, bottom = ScreenInfo().work_area

    monitor_screen_width = right - left
    monitor_screen_height = bottom - top

    total_columns = math.ceil(monitor_screen_width / block_width)
    total_rows = math.ceil(monitor_screen_height / block_height)

    screen = Screen()
    blocks = []
    merged_rows = []

    for row in range(total_rows):
        row_texts = []

        for col in range(total_columns):
            # Calculate absolute screen coordinates
            block_left = left + col * block_width
            block_top = top + row * block_height

            block_right = min(
                block_left + block_width, right
            )
            block_bottom = min(
                block_top + block_height, bottom
            )

            # Extract text from the current block
            text = screen.read_text(
                region=(
                    block_left,
                    block_top,
                    block_right,
                    block_bottom
                ),
                monitor_index=0
            )

            text = str(text).strip() if text else ""

            blocks.append({
                "row": row,
                "column": col,
                "region": (
                    block_left,
                    block_top,
                    block_right,
                    block_bottom
                ),
                "text": text
            })

            if text:
                row_texts.append(text)

        # Merge text across each row
        merged_row = "".join(row_texts)

        if merged_row:
            merged_rows.append(merged_row)

    # Merge rows from top to bottom
    final_text = "".join(merged_rows)
    is_text_present = check(is_text_present,final_text)
    return {
        "work_area": (left, top, right, bottom),
        "monitor_screen_width": monitor_screen_width,
        "monitor_screen_height": monitor_screen_height,
        "is_text_present": is_text_present
    }


if __name__ == "__main__":
    block_width, block_height = 1000, 1000
    is_text_present = "cls"
    results = get_text_from_monitor_screen(block_width, block_height, is_text_present)
    print(results)
