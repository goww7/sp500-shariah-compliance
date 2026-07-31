# S&P 500 Shariah Compliance Dataset

Shariah (Islamic finance) compliance verdicts for the 503 constituents of the
S&P 500, screened across five published methodologies by the
[Halal Terminal](https://www.halalterminal.com) engine.

- **Snapshot generated:** 2026-07-31 (universe from the 2026-07-28 S&P 500 bulk screening run)
- **Rows:** 503 constituents
- **File:** [`data/sp500-compliance.csv`](data/sp500-compliance.csv)
- **Updated:** monthly (first of each month)

## What is in the file

`data/sp500-compliance.csv` has one row per constituent with these columns:

| column | description |
| --- | --- |
| `symbol` | Ticker symbol |
| `name` | Company name |
| `overall_status` | Engine overall verdict: `compliant`, `non_compliant`, or `insufficient_data` |
| `aaoifi` | Verdict under the AAOIFI methodology |
| `djim` | Verdict under the Dow Jones Islamic Market methodology |
| `ftse` | Verdict under the FTSE methodology |
| `msci` | Verdict under the MSCI methodology |
| `sp` | Verdict under the S&P methodology |
| `purification_rate` | Estimated dividend purification rate, in percent |
| `as_of_date` | Date this row's verdict was last computed by the engine |

Each per-methodology column takes one of four values:
`compliant`, `questionable`, `non_compliant`, `insufficient_data`.

Values are copied verbatim from the production screening engine. There is no
re-screening, smoothing, or post-processing in this repository. Where a company
fails the business-activity screen (for example conventional financials or
insurers), `overall_status` is `non_compliant` while the per-methodology financial
columns may read `insufficient_data`, exactly as the engine reports them.

## Methodology summary

Every stock is screened two ways: a business-activity screen (does the company
earn from non-permissible activities such as interest-based finance, alcohol,
gambling, tobacco, adult content, or conventional insurance) and a set of
financial-ratio screens applied under five widely published standards. The five
standards differ mainly in their ratio caps and in whether the denominator is
market capitalization or total assets.

| methodology | debt cap | liquidity / receivables cap | non-permissible income cap | ratio basis |
| --- | --- | --- | --- | --- |
| AAOIFI | 30% | 70% (interest-bearing securities and cash) | 5% | market cap or total assets |
| Dow Jones Islamic Market (DJIM) | 33% | 33% cash and interest-bearing, 33% receivables | 5% | trailing 24-month average market cap |
| FTSE | 33.333% | 33.333% cash and interest-bearing, 50% receivables | 5% | total assets |
| MSCI | 33.333% | 33.333% cash and interest-bearing, 33.333% receivables | 5% | total assets |
| S&P | 33% | 33% cash and interest-bearing, 49% receivables | 5% | market cap |

These thresholds are the published standard rules. Consult the primary standard
documents for the authoritative and complete rule sets.

## Disclaimer

This dataset is informational only. It is **not** a fatwa, not religious advice,
and not investment advice. Compliance methodologies differ, scholars differ, and
a stock's status can change between snapshots. Verify any verdict against your
own scholar or standard before relying on it. No warranty is made as to accuracy
or completeness.

## Source and live data

- Live screening and full per-stock breakdowns: <https://api.halalterminal.com>
- Per-stock pages: `https://www.halalterminal.com/stocks/{symbol}`
  (for example <https://www.halalterminal.com/stocks/AAPL>)

The live pages carry the most current verdict, reasons, ratios, and revenue
breakdowns. This CSV is a monthly point-in-time snapshot.

## Citation

If you use this dataset, please cite **Halal Terminal** and link back to
<https://www.halalterminal.com>.

> Halal Terminal, S&P 500 Shariah Compliance Dataset,
> https://github.com/goww7/sp500-shariah-compliance

## License

Released under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
You may share and adapt the data for any purpose, including commercially, as long
as you give appropriate credit as described above.
