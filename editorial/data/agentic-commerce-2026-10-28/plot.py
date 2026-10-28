#!/usr/bin/env python3
"""Render the three blog figures from preserved observations, without network access."""
import argparse
import json
from pathlib import Path
import xml.etree.ElementTree as ET

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = ROOT / "images" / "charts"
DATA = json.loads((HERE / "observations.json").read_text())
PAPER, INK, MUTED = "#F7F2E8", "#1B2733", "#596772"
TEAL, AMBER, LINE = "#207D74", "#B87316", "#D7CFC0"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 14, "text.parse_math": False,
    "text.color": INK, "axes.labelcolor": MUTED, "xtick.color": MUTED,
    "ytick.color": INK, "figure.facecolor": PAPER, "axes.facecolor": PAPER,
    "svg.fonttype": "none", "svg.hashsalt": "agentic-commerce-20261028",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.spines.left": False, "axes.spines.bottom": False,
})


def frame(title, subtitle, note):
    fig = plt.figure(figsize=(12, 7.2), dpi=100)
    fig.text(.055, .92, title, fontsize=25, weight="bold")
    fig.text(.055, .865, subtitle, fontsize=14, color=MUTED)
    fig.text(.055, .075, note, fontsize=11.5, color=MUTED, linespacing=1.6)
    return fig


def tidy(ax):
    ax.set_axisbelow(True)
    ax.grid(axis="x", color=LINE, linewidth=.8)
    ax.tick_params(axis="both", length=0, pad=9)


def save(fig, stem, title, desc, previews):
    OUT.mkdir(parents=True, exist_ok=True)
    path = OUT / f"{stem}.svg"
    fig.savefig(path, metadata={"Date": None, "Creator": "Codex; Matplotlib", "Title": title, "Description": desc})
    text = path.read_text()
    end = text.index(">", text.index("<svg"))
    text = text[:end] + ' role="img" aria-labelledby="figure-title figure-desc"' + text[end:]
    end = text.index(">", text.index("<svg")) + 1
    from html import escape
    text = text[:end] + f'\n<title id="figure-title">{escape(title)}</title>\n<desc id="figure-desc">{escape(desc)}</desc>' + text[end:]
    ET.fromstring(text)
    path.write_text("\n".join(line.rstrip() for line in text.splitlines()) + "\n")
    if previews:
        previews.mkdir(parents=True, exist_ok=True)
        fig.savefig(previews / f"{stem}.png", dpi=150)
    plt.close(fig)


def retail(previews):
    obs = DATA["retail"]["observations"]
    vals = [100 + o["difference_pct"] for o in obs]
    fig = frame("AI referrals bring more purchase-ready shoppers",
                "U.S. retail conversion index  |  Non-AI referrals = 100 in each period",
                "Sources: Adobe reports, April 16 and August 19, 2026. Checked October 28.\nAI-assisted visits, not proof of autonomous checkout. Three reported snapshots; missing months are not plotted.")
    ax = fig.add_axes([.19, .25, .70, .52])
    ax.barh([2, 1, 0], vals, height=.53, color=[AMBER, TEAL, TEAL])
    ax.set_yticks([2, 1, 0], [o["period"] for o in obs])
    ax.set_xlim(0, 195)
    ax.set_xticks([0, 50, 100, 150])
    ax.axvline(100, color=INK, linestyle=(0, (4, 4)), linewidth=1.5)
    for y, value, item in zip([2, 1, 0], vals, obs):
        ax.text(value + 3, y, f"{value}", va="center", fontsize=22, weight="bold")
        ax.text(3, y, f'{item["difference_pct"]:+d}%', va="center", color="white", weight="bold")
    ax.text(102, 2.62, "Other referrals", fontsize=12, color=MUTED)
    ax.set_ylim(-.65, 2.8)
    tidy(ax)
    save(fig, "agentic-commerce-retail", "AI referrals bring more purchase-ready shoppers",
         "Relative conversion index: March 2025 62; March 2026 142; July 2026 160. Non-AI referrals equal 100 within each period. This is not an absolute conversion rate or proof of causation.", previews)


def payments(previews):
    obs = DATA["x402"]["observations"]
    fig = frame("Payments grew faster than the dollars transferred",
                "Tracked x402 activity  |  July to August 2026, comparable frozen editions",
                "Source: agent economy, July and August reports, edition 1, frozen October 22, 2026.\nSeptember omitted because coverage changed. These transfers do not establish completed services or profit.")
    for position, key, divisor, label, ticks in [
        ([.10, .32, .34, .43], "transactions", 1e6, "Payments (millions)", [0, 5, 10, 15, 20]),
        ([.61, .32, .32, .43], "settled_usd", 1e3, "Dollars transferred (thousands)", [0, 100, 200, 300, 400, 500]),
    ]:
        ax = fig.add_axes(position)
        values = [o[key] / divisor for o in obs]
        ax.bar([0, 1], values, width=.52, color=["#95BAB3", TEAL])
        ax.set_xticks([0, 1], ["July", "August"])
        ax.set_yticks(ticks)
        ax.set_ylim(0, max(ticks))
        ax.set_title(label, fontsize=14, loc="left", pad=20)
        ax.set_axisbelow(True)
        ax.grid(axis="y", color=LINE, linewidth=.8)
        ax.tick_params(length=0, pad=8)
        for i, value in enumerate(values):
            text = f"{value:.2f}M" if key == "transactions" else f"${obs[i][key]:,}"
            ax.text(i, value + max(ticks)*.035, text, ha="center", fontsize=17, weight="bold")
    growth_n = 100*(obs[1]["transactions"]/obs[0]["transactions"]-1)
    growth_v = 100*(obs[1]["settled_usd"]/obs[0]["settled_usd"]-1)
    means = [100*o["settled_usd"]/o["transactions"] for o in obs]
    fig.text(.10, .205, f"Count: +{growth_n:.1f}%    |    Dollars: +{growth_v:.1f}%", fontsize=15, weight="bold", color=TEAL)
    fig.text(.10, .155, f"Mean value per transfer: {means[0]:.2f}¢ → {means[1]:.2f}¢  (not a typical service price)", fontsize=13.5)
    save(fig, "agentic-commerce-payments", "Payments grew faster than dollars transferred",
         "July: 6,010,540 payments and $238,084. August: 17,855,635 payments and $437,476. Count grew 197.1 percent, dollars 83.7 percent. Mean transfer fell from 3.96 to 2.45 cents. Panels have different labeled units.", previews)


def screening(previews):
    d = DATA["screening"]
    shares = [100*d["payments_pass"]/d["payments_total"], 100*d["usd_pass"]/d["usd_total"]]
    fig = frame("Recorded activity still needs an economic explanation",
                "One Base x402 sample  |  October 9–16, 2026  |  Share of each sample total",
                "Source: Agent Pay Tracker, snapshot generated October 17, 2026. Checked October 28.\nHeuristic screening, not an audit: flagged can be legitimate; passing does not prove an AI purchase.")
    ax = fig.add_axes([.22, .31, .70, .43])
    y = [1, 0]
    ax.barh(y, shares, color=TEAL, height=.50, label="Passed all screens")
    ax.barh(y, [100-s for s in shares], left=shares, color="#E2C08E", height=.50, label="Flagged by screens")
    ax.set_xlim(0, 100)
    ax.set_ylim(-.6, 1.6)
    ax.set_yticks(y, ["Payment count", "Dollar value"])
    ax.set_xticks([0, 25, 50, 75, 100])
    ax.xaxis.set_major_formatter(PercentFormatter(100))
    for yi, share in zip(y, shares):
        ax.text(share/2, yi, f"{share:.1f}%", ha="center", va="center", color="white", fontsize=17, weight="bold")
        ax.text(share+(100-share)/2, yi, f"{100-share:.1f}%", ha="center", va="center", color=INK, fontsize=17)
    tidy(ax)
    ax.legend(loc="lower left", bbox_to_anchor=(-.01, 1.01), ncol=2, frameon=False, fontsize=13)
    fig.text(.22, .22, "Passed: 189,329 of 442,419 payments", fontsize=14, color=TEAL)
    fig.text(.22, .175, "Passed: $23,150 of $270,548 transferred", fontsize=14, color=TEAL)
    save(fig, "agentic-commerce-screening", "Recorded activity still needs an economic explanation",
         "42.8 percent of payment count and 8.6 percent of dollar value passed the tracker's screens; 57.2 and 91.4 percent were flagged. Passing is not verified commerce and flagged is not proven fraud.", previews)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()
    retail(args.preview_dir)
    payments(args.preview_dir)
    screening(args.preview_dir)
    print("Wrote three chart SVGs from observations.json")
