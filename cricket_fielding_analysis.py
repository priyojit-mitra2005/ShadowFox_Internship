"""
Cricket Fielding Analysis System
=================================
Analyses fielding performance for T20 match players using the formula:
PS = (CP×1) + (GT×1) + (C×3) + (DC×-3) + (ST×3) + (RO×3) + (MRO×-2) + (DH×2) + RS

Where:
  CP  = Clean Picks        (+1)
  GT  = Good Throws        (+1)
  C   = Catches            (+3)
  DC  = Dropped Catches    (-3)
  ST  = Stumpings          (+3)
  RO  = Run Outs           (+3)
  MRO = Missed Run Outs    (-2)
  DH  = Direct Hits        (+2)
  RS  = Runs Saved/Conceded (+/-)

Includes optional CSV export (pure Python `csv` module — no openpyxl/Excel).
"""

import csv
import os

# ─────────────────────────────────────────────────────────────────────────────
# WEIGHTS (as per task PDF)
# ─────────────────────────────────────────────────────────────────────────────
WEIGHTS = {
    "CP":  1,
    "GT":  1,
    "C":   3,
    "DC": -3,
    "ST":  3,
    "RO":  3,
    "MRO":-2,
    "DH":  2,
}

# ─────────────────────────────────────────────────────────────────────────────
# DATASET
# Each record: (match, innings, team, player, ball, position,
#               description, CP, GT, C, DC, ST, RO, MRO, DH, RS, over, venue)
# ─────────────────────────────────────────────────────────────────────────────
FIELDING_DATA = [
    # ── Rilee Russouw (expected PS ≈ 10 per PDF sample) ──────────────────────
    (1,"1st","Team A","Rilee Russouw","1.2","Cover",
     "Clean pick, good throw to keeper",          1,1,0,0,0,0,0,0, 2,1,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","2.4","Mid-off",
     "Direct hit attempt, clean field",            1,1,0,0,0,0,0,1, 0,2,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","3.1","Point",
     "Caught at point off mistimed shot",          0,0,1,0,0,0,0,0, 3,3,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","4.3","Cover",
     "Clean pick, accurate throw",                 1,1,0,0,0,0,0,0, 2,4,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","5.5","Outfield",
     "Missed run-out opportunity",                 0,0,0,0,0,0,1,0,-3,5,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","7.2","Slip",
     "Dropped catch in slip cordon",               0,0,0,1,0,0,0,0,-3,7,"Dubai"),
    (1,"1st","Team A","Rilee Russouw","9.4","Cover",
     "Clean pick, saves 2 runs",                   1,0,0,0,0,0,0,0, 2,9,"Dubai"),

    # ── Phil Salt (expected PS ≈ 2 per PDF sample) ────────────────────────────
    (1,"1st","Team A","Phil Salt","1.3","Keeper",
     "Stumping — clean take",                      0,0,0,0,1,0,0,0,-1,1,"Dubai"),
    (1,"1st","Team A","Phil Salt","2.1","Keeper",
     "Clean pick direct hit",                      1,0,0,0,0,0,0,1, 3,2,"Dubai"),
    (1,"1st","Team A","Phil Salt","3.4","Keeper",
     "Missed stumping chance",                     0,0,0,0,0,0,1,0,-3,3,"Dubai"),
    (1,"1st","Team A","Phil Salt","6.2","Keeper",
     "Catch behind the wicket",                    0,0,1,0,0,0,0,0, 3,6,"Dubai"),
    (1,"1st","Team A","Phil Salt","8.1","Keeper",
     "Good throw from boundary",                   0,1,0,0,0,0,0,0, 0,8,"Dubai"),

    # ── Yash Dhull (expected PS ≈ 11 per PDF sample) ─────────────────────────
    (1,"1st","Team A","Yash Dhull","1.1","Mid-on",
     "Clean field, accurate return",               1,0,0,0,0,0,0,0, 3,1,"Dubai"),
    (1,"1st","Team A","Yash Dhull","2.2","Square leg",
     "Direct hit run-out",                         0,0,0,0,0,1,0,0, 3,2,"Dubai"),
    (1,"1st","Team A","Yash Dhull","4.4","Mid-wicket",
     "Clean pick stops boundary",                  1,0,0,0,0,0,0,0, 2,4,"Dubai"),
    (1,"1st","Team A","Yash Dhull","5.2","Fine leg",
     "Excellent diving catch",                     0,0,1,0,0,0,0,0, 3,5,"Dubai"),
    (1,"1st","Team A","Yash Dhull","7.3","Mid-on",
     "Clean field, run-out direct hit",            1,1,0,0,0,1,0,1, 3,7,"Dubai"),
    (1,"1st","Team A","Yash Dhull","10.5","Long-on",
     "Tough catch on boundary",                    0,0,1,0,0,0,0,0, 3,10,"Dubai"),

    # ── Axer Patel (expected PS ≈ 11 per PDF sample) ─────────────────────────
    (1,"1st","Team A","Axer Patel","2.3","Cover",
     "Clean field, good throw",                    1,0,0,0,0,0,0,0, 3,2,"Dubai"),
    (1,"1st","Team A","Axer Patel","3.5","Mid-off",
     "Missed run-out, close attempt",              0,1,0,0,0,0,1,0,-1,3,"Dubai"),
    (1,"1st","Team A","Axer Patel","5.4","Long-on",
     "Clean field, saved 3",                       1,1,0,0,0,0,0,0, 3,5,"Dubai"),
    (1,"1st","Team A","Axer Patel","7.1","Extra cover",
     "Direct hit run-out",                         0,0,0,0,0,1,0,0, 3,7,"Dubai"),
    (1,"1st","Team A","Axer Patel","9.1","Slip",
     "Dropped slip catch",                         0,0,0,1,0,0,0,0,-3,9,"Dubai"),

    # ── Lalit Yadav (expected PS ≈ 6 per PDF sample) ─────────────────────────
    (1,"1st","Team A","Lalit Yadav","1.4","Point",
     "Clean field, run saved",                     1,0,0,0,0,0,0,0, 2,1,"Dubai"),
    (1,"1st","Team A","Lalit Yadav","3.2","Cover",
     "Good throw, near-run-out",                   0,1,0,0,0,0,0,0, 0,3,"Dubai"),
    (1,"1st","Team A","Lalit Yadav","6.4","Mid-off",
     "Clean field, 2 runs saved",                  1,0,0,0,0,0,0,0, 2,6,"Dubai"),
    (1,"1st","Team A","Lalit Yadav","8.3","Deep mid-wkt",
     "Missed run-out",                             0,0,0,0,0,0,1,0,-2,8,"Dubai"),
    (1,"1st","Team A","Lalit Yadav","10.2","Long-off",
     "Fumble, conceded extra run",                 0,0,0,0,0,0,0,0,-2,10,"Dubai"),

    # ── Aman Khan (expected PS ≈ 6 per PDF sample) ───────────────────────────
    (1,"1st","Team A","Aman Khan","2.5","Fine leg",
     "Clean pick, direct hit attempt",             1,0,0,0,0,0,0,1, 0,2,"Dubai"),
    (1,"1st","Team A","Aman Khan","4.1","Square leg",
     "Good throw prevents run",                    0,1,0,0,0,0,0,0, 1,4,"Dubai"),
    (1,"1st","Team A","Aman Khan","6.3","Third man",
     "Clean boundary save",                        1,0,0,0,0,0,0,0, 3,6,"Dubai"),
    (1,"1st","Team A","Aman Khan","8.5","Deep square",
     "Dropped catch",                              0,0,0,1,0,0,0,0,-3,8,"Dubai"),
    (1,"1st","Team A","Aman Khan","11.1","Point",
     "Run-out direct hit",                         0,0,0,0,0,1,0,0, 3,11,"Dubai"),
]


# ─────────────────────────────────────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────────────────────────────────────

def calculate_ps(stats: dict) -> int:
    """Calculate Performance Score from a player's aggregated stats dict."""
    return (
        stats["CP"]  * WEIGHTS["CP"]  +
        stats["GT"]  * WEIGHTS["GT"]  +
        stats["C"]   * WEIGHTS["C"]   +
        stats["DC"]  * WEIGHTS["DC"]  +
        stats["ST"]  * WEIGHTS["ST"]  +
        stats["RO"]  * WEIGHTS["RO"]  +
        stats["MRO"] * WEIGHTS["MRO"] +
        stats["DH"]  * WEIGHTS["DH"]  +
        stats["RS"]
    )


def aggregate_players(data: list) -> dict:
    """Aggregate raw fielding events into per-player stat dictionaries."""
    players = {}
    for row in data:
        (match, inn, team, player, ball, pos, desc,
         cp, gt, c, dc, st, ro, mro, dh, rs, over, venue) = row

        if player not in players:
            players[player] = {
                "CP":0,"GT":0,"C":0,"DC":0,"ST":0,
                "RO":0,"MRO":0,"DH":0,"RS":0,"events":[]
            }
        p = players[player]
        p["CP"]  += cp;  p["GT"]  += gt;  p["C"]   += c
        p["DC"]  += dc;  p["ST"]  += st;  p["RO"]  += ro
        p["MRO"] += mro; p["DH"]  += dh;  p["RS"]  += rs
        p["events"].append(row)

    return players


def progress_bar(value: int, max_val: int, width: int = 20, char: str = "█") -> str:
    """Return a text progress bar."""
    if max_val == 0:
        return "─" * width
    filled = int((value / max_val) * width)
    filled = max(0, min(filled, width))
    return char * filled + "░" * (width - filled)


def rating_label(ps: int) -> str:
    """Return a star rating label based on performance score."""
    if ps >= 15:  return "★★★★★  OUTSTANDING"
    if ps >= 10:  return "★★★★☆  EXCELLENT"
    if ps >= 6:   return "★★★☆☆  GOOD"
    if ps >= 2:   return "★★☆☆☆  AVERAGE"
    if ps >= 0:   return "★☆☆☆☆  BELOW AVERAGE"
    return          "☆☆☆☆☆  POOR"


def ps_formula_string(p: dict) -> str:
    """Return the expanded PS formula string for display."""
    parts = [
        f"({p['CP']}×1)",
        f"({p['GT']}×1)",
        f"({p['C']}×3)",
        f"({p['DC']}×-3)",
        f"({p['ST']}×3)",
        f"({p['RO']}×3)",
        f"({p['MRO']}×-2)",
        f"({p['DH']}×2)",
        f"{p['RS']:+d}",
    ]
    return " + ".join(parts)


def ps_simplified(p: dict) -> str:
    """Return the simplified PS formula string."""
    vals = [
        p["CP"]*1, p["GT"]*1, p["C"]*3, p["DC"]*-3,
        p["ST"]*3, p["RO"]*3, p["MRO"]*-2, p["DH"]*2, p["RS"]
    ]
    return " + ".join(f"{v:+d}" if i > 0 else str(v) for i, v in enumerate(vals))


# ─────────────────────────────────────────────────────────────────────────────
# CSV EXPORT  (pure Python `csv` module — no Excel libraries used)
# ─────────────────────────────────────────────────────────────────────────────

def export_raw_data_csv(data: list, filepath: str):
    """Write the ball-by-ball raw fielding log to a CSV file."""
    headers = [
        "Match No.","Innings","Team","Player Name","Ball Count","Position",
        "Short Description","CP","GT","C","DC","ST","RO","MRO","DH",
        "Runs Saved","Over","Venue"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in data:
            writer.writerow(row)
    print(f"  ✔  Raw data exported to: {filepath}")


def export_performance_scores_csv(players: dict, filepath: str):
    """Write the aggregated, ranked performance scores to a CSV file."""
    scored = sorted(
        [(pl, p, calculate_ps(p)) for pl, p in players.items()],
        key=lambda x: x[2], reverse=True
    )
    headers = [
        "Rank","Player","CP","GT","C","DC","ST","RO","MRO","DH",
        "Runs Saved","Balls Involved","Performance Score (PS)","Rating"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for rank, (player, p, ps) in enumerate(scored, 1):
            writer.writerow([
                rank, player, p["CP"], p["GT"], p["C"], p["DC"], p["ST"],
                p["RO"], p["MRO"], p["DH"], p["RS"], len(p["events"]),
                ps, rating_label(ps)
            ])
    print(f"  ✔  Performance scores exported to: {filepath}")


def export_player_breakdown_csv(players: dict, filepath: str):
    """Write the full action-by-action breakdown (all players, one file) to CSV."""
    headers = [
        "Player","Over","Ball","Position","Description","Actions",
        "Runs Saved","PS Contribution","Running PS"
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for player, p in players.items():
            running_ps = 0
            for row in p["events"]:
                (match, inn, team, pl, ball, pos, desc,
                 cp, gt, c, dc, st, ro, mro, dh, rs, over, venue) = row

                parts = []
                if cp:  parts.append(f"CP+{cp}")
                if gt:  parts.append(f"GT+{gt}")
                if c:   parts.append(f"C+{c}")
                if dc:  parts.append(f"DC-{dc}")
                if st:  parts.append(f"ST+{st}")
                if ro:  parts.append(f"RO+{ro}")
                if mro: parts.append(f"MRO-{mro}")
                if dh:  parts.append(f"DH+{dh}")
                action_str = ", ".join(parts) if parts else "Fielded"

                contrib = (cp*1 + gt*1 + c*3 + dc*(-3) + st*3 +
                           ro*3 + mro*(-2) + dh*2 + rs)
                running_ps += contrib

                writer.writerow([
                    player, over, ball, pos, desc, action_str,
                    rs, contrib, running_ps
                ])
    print(f"  ✔  Player breakdown exported to: {filepath}")


def export_all_csv(data: list, players: dict, out_dir: str = "."):
    """Export all three CSV reports into the given directory."""
    os.makedirs(out_dir, exist_ok=True)
    print("\n" + "=" * 80)
    print("  EXPORTING CSV REPORTS")
    print("=" * 80)
    export_raw_data_csv(data, os.path.join(out_dir, "raw_fielding_data.csv"))
    export_performance_scores_csv(players, os.path.join(out_dir, "performance_scores.csv"))
    export_player_breakdown_csv(players, os.path.join(out_dir, "player_breakdown.csv"))
    print("=" * 80)


# ─────────────────────────────────────────────────────────────────────────────
# PRINT SECTIONS
# ─────────────────────────────────────────────────────────────────────────────

SEP  = "=" * 80
SEP2 = "-" * 80
SEP3 = "·" * 80


def print_header():
    print(SEP)
    print("  🏏  CRICKET FIELDING ANALYSIS SYSTEM  |  T20 Match #1  |  Dubai")
    print("  Formula: PS = (CP×1)+(GT×1)+(C×3)+(DC×-3)+(ST×3)+(RO×3)+(MRO×-2)+(DH×2)+RS")
    print(SEP)


def print_weight_reference():
    print("\n" + SEP2)
    print("  WEIGHT REFERENCE TABLE")
    print(SEP2)
    table = [
        ("CP",  "Clean Pick",       "+1",  "Fielder picks up the ball cleanly"),
        ("GT",  "Good Throw",       "+1",  "Accurate throw that pressures the batter"),
        ("C",   "Catch",            "+3",  "Successfully completed catch"),
        ("DC",  "Dropped Catch",    "−3",  "Missed catch opportunity"),
        ("ST",  "Stumping",         "+3",  "Keeper stumps out a batsman"),
        ("RO",  "Run Out",          "+3",  "Successful run-out dismissal"),
        ("MRO", "Missed Run Out",   "−2",  "Failed run-out attempt"),
        ("DH",  "Direct Hit",       "+2",  "Ball hits stumps directly"),
        ("RS",  "Runs Saved",       "+/−", "Runs saved (+) or conceded (−)"),
    ]
    print(f"  {'Code':<6} {'Action':<20} {'Wt':>4}   {'Description'}")
    print("  " + "─"*66)
    for code, action, wt, desc in table:
        print(f"  {code:<6} {action:<20} {wt:>4}   {desc}")
    print(SEP2)


def print_raw_data(data: list):
    print("\n" + SEP)
    print("  RAW FIELDING DATA  —  Ball-by-Ball Log")
    print(SEP)
    print(f"  {'#':<3} {'Player':<18} {'Ball':<6} {'Position':<14} "
          f"{'CP':>3}{'GT':>3}{'C':>3}{'DC':>3}{'ST':>3}"
          f"{'RO':>3}{'MRO':>4}{'DH':>3}{'RS':>4}   Description")
    print("  " + "─"*77)
    for i, row in enumerate(data, 1):
        (match, inn, team, player, ball, pos, desc,
         cp, gt, c, dc, st, ro, mro, dh, rs, over, venue) = row
        desc_short = desc[:35] + "…" if len(desc) > 35 else desc
        print(f"  {i:<3} {player:<18} {ball:<6} {pos:<14} "
              f"{cp:>3}{gt:>3}{c:>3}{dc:>3}{st:>3}"
              f"{ro:>3}{mro:>4}{dh:>3}{rs:>+4}   {desc_short}")
    print(f"\n  Total events recorded: {len(data)}")
    print(SEP2)


def print_player_breakdown(players: dict):
    print("\n" + SEP)
    print("  PLAYER-BY-PLAYER BREAKDOWN  —  Action Details & Running PS")
    print(SEP)

    for player, p in players.items():
        ps = calculate_ps(p)
        print(f"\n  {'▶':>2}  {player.upper():<20}  |  Final PS = {ps:+d}  |  {rating_label(ps)}")
        print("  " + "─"*72)
        print(f"  {'Over':<6} {'Ball':<7} {'Position':<14} "
              f"{'Actions':<28} {'RS':>4} {'Contrib':>7} {'Running PS':>10}")
        print("  " + "·"*72)

        running_ps = 0
        for row in p["events"]:
            (match, inn, team, pl, ball, pos, desc,
             cp, gt, c, dc, st, ro, mro, dh, rs, over, venue) = row

            # Build actions label
            parts = []
            if cp:  parts.append(f"CP+{cp}")
            if gt:  parts.append(f"GT+{gt}")
            if c:   parts.append(f"C+{c}")
            if dc:  parts.append(f"DC-{dc}")
            if st:  parts.append(f"ST+{st}")
            if ro:  parts.append(f"RO+{ro}")
            if mro: parts.append(f"MRO-{mro}")
            if dh:  parts.append(f"DH+{dh}")
            action_str = ", ".join(parts) if parts else "Fielded"

            contrib     = (cp*1 + gt*1 + c*3 + dc*(-3) + st*3 +
                           ro*3 + mro*(-2) + dh*2 + rs)
            running_ps += contrib
            rs_sign     = f"{rs:+d}"
            c_sign      = f"{contrib:+d}"
            r_sign      = f"{running_ps:+d}"

            print(f"  {str(over):<6} {ball:<7} {pos:<14} "
                  f"{action_str:<28} {rs_sign:>4} {c_sign:>7} {r_sign:>10}")

        print("  " + "─"*72)
        print(f"  {'TOTAL':<6} {'':>7} {'':>14} {'':>28} "
              f"{p['RS']:>+4} {'':>7} {ps:>+10}")

    print("\n" + SEP2)


def print_performance_scores(players: dict):
    print("\n" + SEP)
    print("  PERFORMANCE SCORES  —  PS Formula & Rankings")
    print(SEP)

    # Compute and sort
    scored = []
    for player, p in players.items():
        ps = calculate_ps(p)
        scored.append((player, p, ps))
    scored.sort(key=lambda x: x[2], reverse=True)

    max_ps = max(s[2] for s in scored) if scored else 1

    print(f"\n  {'Rank':<6} {'Player':<18} {'PS':>5}  {'Bar (max='+str(max_ps)+')':<25} Rating")
    print("  " + "─"*72)
    for rank, (player, p, ps) in enumerate(scored, 1):
        bar   = progress_bar(max(ps, 0), max(max_ps, 1), width=22)
        medal = {1:"🥇",2:"🥈",3:"🥉"}.get(rank, f"  {rank}.")
        print(f"  {medal:<5}  {player:<18} {ps:>5}  {bar}  {rating_label(ps)}")

    print("\n" + SEP2)

    # Expanded formula for each player
    print("\n  PS FORMULA BREAKDOWN PER PLAYER")
    print("  " + "─"*72)
    for player, p, ps in scored:
        print(f"\n  {player}")
        print(f"    Expanded : PS = {ps_formula_string(p)}")
        print(f"    Values   : PS = {ps_simplified(p)}")
        print(f"    Result   : PS = {ps}")

    print("\n" + SEP2)


def print_stat_comparison(players: dict):
    print("\n" + SEP)
    print("  COMPARATIVE STAT SUMMARY  —  All Players Side by Side")
    print(SEP)

    scored = sorted(
        [(pl, p, calculate_ps(p)) for pl, p in players.items()],
        key=lambda x: x[2], reverse=True
    )
    keys = ["CP","GT","C","DC","ST","RO","MRO","DH","RS"]

    # Header
    header = f"  {'Stat':<6}"
    for player, _, _ in scored:
        short = player.split()[0][:10]
        header += f"  {short:>10}"
    print(header)
    print("  " + "─"*66)

    for key in keys:
        row = f"  {key:<6}"
        for player, p, _ in scored:
            val = p[key]
            row += f"  {val:>+10}"
        print(row)

    # PS total row
    print("  " + "─"*66)
    ps_row = f"  {'PS':<6}"
    for player, p, ps in scored:
        ps_row += f"  {ps:>+10}"
    print(ps_row)

    # Events row
    ev_row = f"  {'Events':<6}"
    for player, p, _ in scored:
        ev_row += f"  {len(p['events']):>10}"
    print(ev_row)
    print(SEP2)


def print_insights(players: dict):
    print("\n" + SEP)
    print("  KEY INSIGHTS & RECOMMENDATIONS")
    print(SEP)

    scored = sorted(
        [(pl, p, calculate_ps(p)) for pl, p in players.items()],
        key=lambda x: x[2], reverse=True
    )

    best_pl,  best_p,  best_ps  = scored[0]
    worst_pl, worst_p, worst_ps = scored[-1]

    total_catches   = sum(p["C"]   for _, p, _ in scored)
    total_drops     = sum(p["DC"]  for _, p, _ in scored)
    total_runouts   = sum(p["RO"]  for _, p, _ in scored)
    total_rs        = sum(p["RS"]  for _, p, _ in scored)
    drop_rate       = total_drops / (total_catches + total_drops) * 100 if (total_catches + total_drops) > 0 else 0
    avg_ps          = sum(ps for _, _, ps in scored) / len(scored)

    print(f"\n  📊  Match: T20 Match #1  |  Venue: Dubai  |  Innings: 1st")
    print(f"  📋  Total fielding events : {len(FIELDING_DATA)}")
    print(f"  👥  Players analysed      : {len(players)}")
    print(f"  📈  Average PS            : {avg_ps:.1f}")
    print()
    print(f"  🥇  Best performer  : {best_pl:<18}  PS = {best_ps:+d}  ({rating_label(best_ps)})")
    print(f"  ⚠️   Needs work      : {worst_pl:<18}  PS = {worst_ps:+d}  ({rating_label(worst_ps)})")
    print()
    print(f"  🎯  Total catches    : {total_catches}   |  Dropped : {total_drops}  "
          f"(Drop rate: {drop_rate:.1f}%)")
    print(f"  🏃  Total run-outs   : {total_runouts}")
    print(f"  💰  Total runs saved : {total_rs:+d}")
    print()

    # Recommendations
    print("  RECOMMENDATIONS")
    print("  " + "─"*50)
    for player, p, ps in scored:
        issues = []
        if p["DC"] > 0:
            issues.append(f"Reduce dropped catches ({p['DC']} drops cost {p['DC']*3} pts)")
        if p["MRO"] > 0:
            issues.append(f"Improve run-out execution ({p['MRO']} missed = {p['MRO']*2} pts lost)")
        if p["RS"] < 0:
            issues.append(f"Tighten boundary fielding ({p['RS']} runs conceded)")
        if p["DH"] > 0:
            issues.append(f"Good direct-hit instinct — keep it up! ({p['DH']} DH)")
        if p["C"] >= 2:
            issues.append(f"Strong catcher — {p['C']} catches secured")

        status = "✅" if ps >= 8 else ("⚠️ " if ps >= 3 else "❌")
        print(f"\n  {status}  {player} (PS={ps:+d})")
        for issue in issues:
            print(f"      • {issue}")
        if not issues:
            print("      • Solid all-round performance, no major concerns.")

    print("\n" + SEP)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    players = aggregate_players(FIELDING_DATA)

    print_header()
    print_weight_reference()
    print_raw_data(FIELDING_DATA)
    print_player_breakdown(players)
    print_performance_scores(players)
    print_stat_comparison(players)
    print_insights(players)

    # Export CSV reports (pure Python csv module — no Excel libraries)
    export_all_csv(FIELDING_DATA, players, out_dir="cricket_reports")


if __name__ == "__main__":
    main()
