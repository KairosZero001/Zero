def print_stats(stats, elapsed):

    print()

    print(
        "Load:",
        stats.get("load_duration", 0) / 1e9,
        "s"
    )

    print(
        "Prompt:",
        stats.get("prompt_eval_duration", 0) / 1e9,
        "s"
    )

    print(
        "Generate:",
        stats.get("eval_duration", 0) / 1e9,
        "s"
    )

    print(
        "Total:",
        stats.get("total_duration", 0) / 1e9,
        "s"
    )

    print(f"\n({elapsed:.2f} seconds)\n")