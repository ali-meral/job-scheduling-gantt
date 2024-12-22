import matplotlib.pyplot as plt
import pandas as pd
import io


# function to plot a gantt chart from energy scheduling output
def plot_gantt_chart(data):
    # parse the input data
    lines = data.strip().splitlines()  # split input into lines
    num_jobs, makespan, total_energy = map(float, lines[:3])  # extract metadata
    df = pd.read_csv(
        io.StringIO("\n".join(lines[3:])),  # load job schedule data
        sep=r"\s+",  # split by whitespace
        names=["job", "machine", "pstate", "start", "end"],  # column names
        engine="python",  # use python engine for regex
    )

    # initialize plot
    fig, ax = plt.subplots(figsize=(12, 5))  # set figure size
    max_end_time = df["end"].max()  # get max end time
    max_machine_id = df["machine"].max()  # get max machine id

    # iterate over each machine and plot its schedule
    for machine_id in range(1, int(max_machine_id) + 1):
        machine_jobs = df[df["machine"] == machine_id].sort_values(
            by="start"
        )  # filter jobs for this machine
        last_end_time = 0  # track the last job's end time
        y_pos = (
            max_machine_id - machine_id
        )  # vertical position of the machine in the chart

        # iterate over each job assigned to this machine
        for _, row in machine_jobs.iterrows():
            start, end, job, pstate = (
                row["start"],
                row["end"],
                row["job"],
                row["pstate"],
            )

            # plot idle time if there's a gap between jobs
            if start > last_end_time:
                idle_duration = start - last_end_time
                ax.barh(
                    y_pos,
                    idle_duration,
                    left=last_end_time,
                    height=0.8,
                    color="white",
                    edgecolor="black",  # idle blocks are white with black border
                )

            # plot the job block
            ax.barh(y_pos, end - start, left=start, height=0.8, edgecolor="black")
            ax.text(
                start + (end - start) / 2,
                y_pos,
                f"J{int(job)}\nP{int(pstate)}",  # label job and pstate
                va="center",
                ha="center",
                color="white",
                fontsize=12,
            )
            last_end_time = end  # update last end time

        # plot idle time after the last job if it doesn't reach max_end_time
        if last_end_time < max_end_time:
            idle_duration = max_end_time - last_end_time
            ax.barh(
                y_pos,
                idle_duration,
                left=last_end_time,
                height=0.8,
                color="white",
                edgecolor="black",
            )

    # set axis labels and formatting
    ax.set_yticks(range(int(max_machine_id)))
    ax.set_yticklabels(
        [f"m{i}" for i in range(int(max_machine_id), 0, -1)], fontsize=10
    )
    ax.set_xlabel("Time (s)", fontsize=12)
    ax.set_xlim(0, max_end_time)
    plt.grid(True, axis="x", linestyle="--", alpha=0.7)
    plt.show()

    # print metadata for summary
    print(
        f"Number of jobs: {int(num_jobs)}\nMakespan: {makespan:.9f} s\nTotal Energy: {total_energy:.9f} J"
    )


# example usage with sample input
example_output = """
24
182.165143120
10909.758512185
1 3 2 85.944205423 125.581373469
2 3 2 133.655005921 180.050509839
3 6 2 32.456743487 34.081264166
4 2 5 0.320430096 41.769779602
5 2 4 91.110499150 153.333121457
6 5 2 108.853439395 182.165143120
7 5 3 94.727485295 108.337367831
8 6 2 36.369490077 52.612816299
9 5 3 0.220315217 58.522393340
10 4 2 85.468638343 120.475434664
11 3 5 0.010025918 10.891968545
12 4 2 31.764382373 85.072641497
13 4 2 1.339796014 30.916094353
14 6 2 127.942848482 173.159508048
15 2 2 157.171955850 181.575820768
16 6 6 0.024471822 30.622996591
17 6 4 52.962212664 123.310264101
18 3 2 128.226316554 132.560601861
19 3 4 13.391173151 80.227678496
20 1 2 4.031571115 38.130498912
21 5 6 65.664582696 94.678094698
22 2 5 46.678175622 87.739659002
23 1 2 106.949543269 162.143657621
24 1 5 40.273501158 94.170963825
"""

plot_gantt_chart(example_output)