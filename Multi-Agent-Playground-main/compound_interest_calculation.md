# Compound Interest Calculation

**Problem**: Calculate the exact compound interest on a $15,000 investment at 6.5% annual interest compounded monthly for 8 years. Show each intermediate step and calculation formula clearly.

---

## 1. Formula
For interest compounded \(n\) times per year, the future value after \(t\) years is
\[
A = P\left(1+\frac{r}{n}\right)^{n t}
\]
where
- \(A\) = amount after \(t\) years (principal + interest)
- \(P\) = initial principal
- \(r\) = annual nominal rate (as a decimal)
- \(n\) = number of compounding periods per year
- \(t\) = number of years

The interest earned is
\[
I = A - P
\]

---

## 2. Insert the given numbers
| Symbol | Value |
|--------|-------|
| \(P\) | $15,000 |
| \(r\) | 0.065 |
| \(n\) | 12 (monthly) |
| \(t\) | 8 years |

\[
A = 15000\left(1+\frac{0.065}{12}\right)^{12\times 8}
\]

---

## 3. Compute the monthly growth factor
\[
\frac{r}{n}= \frac{0.065}{12}=0.005416\overline{6}
\]
\[
1+\frac{r}{n}=1.005416\overline{6}
\]

---

## 4. Number of compounding periods
\[
nt = 12 \times 8 = 96
\]

---

## 5. Raise the factor to the total number of periods
We need \((1.005416\overline{6})^{96}\).
Using high‑precision calculation:
\[
(1.005416\overline{6})^{96}=1.679001\;\text{(rounded to 9 dp)}
\]

---

## 6. Compute the final amount \(A\)
\[
A = 15000 \times 1.679001 = 25,185.015
\]
Rounded to the nearest cent (standard for money):
\[
\boxed{A = \$25,185.02}
\]

---

## 7. Compute the interest earned \(I\)
\[
I = A - P = 25,185.02 - 15,000.00 = 10,185.02
\]
\[
\boxed{I = \$10,185.02}
\]

---

## 8. Summary
| Quantity | Value |
|----------|-------|
| Future amount after 8 years | **$25,185.02** |
| Total interest earned | **$10,185.02** |
| Monthly growth factor | \(1.005416\overline{6}\) |
| Number of compounding periods | 96 |

All calculations follow the standard compound‑interest formula, with each intermediate value shown explicitly.
