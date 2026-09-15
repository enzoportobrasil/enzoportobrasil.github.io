# BGEV animation: maintenance and validation

Integrated before Selected figures in `research/spatial-extremes.html`. No publication or backend. Original figures and existing page content are preserved.

## Files and local preview

- `assets/js/bgev-math.mjs`: validated parameter domain, transformation, inverse, GEV and BGEV PDF/CDF/quantile/support, seeded spatial draws.
- `assets/js/bgev-animation.mjs`: SVG rendering, narrative, controls and accessibility.
- `assets/css/bgev-animation.css`: scoped styling using the site's font variables.
- `assets/img/research/02-spatial-extremes/bgev-construction.svg`: static fallback, present before module initialization and when scripts are disabled/unavailable.

Serve the repository over HTTP (ES modules require HTTP rather than `file:`): `python3 -m http.server 8765 --bind 127.0.0.1`. Open `/research/spatial-extremes.html#bgev-animation`.

Run `node tests/bgev-math.test.mjs` and `node tests/bgev-reference.test.mjs`. Rebuild the fallback after mathematical changes with `node tests/build-bgev-fallback.mjs`. Node is only a maintenance dependency; the website needs no build or runtime dependency.

## Mathematical choices

Source: supplied 2026 dissertation, §2.1.2, equations 2.6–2.12; §3.2; explicit links in equation 3.18 (printed page 46). BGEV means Bimodal Generalized Extreme Value. Every intermediate curve is computed from the transformation and Jacobian, never a mixture or geometric morph.

The explicit ξ=0 branch uses the Gumbel formula. `log1p` and `expm1` stabilize ξ near zero; log-density avoids overflow times underflow. δ=0 has an exact separate branch, including y=μ. For δ>0, f(μ)=0. The mathematical library accepts δ>−1; negative δ has an infinite density at μ. The interactive graph is restricted to [0,3]. At finite upper support endpoints the library returns the interior limiting density (0 for −1<ξ<0, transformed 1/ϱ for ξ=−1, infinity for ξ<−1), and zero strictly outside. An endpoint value does not change probabilities.

The movie starts at ξ=μ=0, ϱ=1. From 3–7 s, fixed quantiles and the correctly normalized density move as δ rises from 0 to 1; from 7–12 s, the Jacobian is emphasized and δ continues to 3. This continuous sweep avoids resetting the transported quantiles between the two explanatory stages. Spatial locations A/B/C occupy the final six seconds. The final 0.35 seconds dim editorially before resetting the story. The blue reference always remains the initial Gumbel and is explicitly labelled, including during shape presets.

Spatial simulation: seed 2026; exact Cholesky draws of four independent finite-dimensional GPs at (0.18,0.68), (0.50,0.28), (0.82,0.62). Exponential correlation exp(−distance/0.55); latent means (0,0,0,0.2), SDs (0.35,0.55,0.18,0.28), in ξ/μ/ϱ/δ order. Natural links are ξ=0.7 tanh(gξ), μ=gμ, ϱ=exp(gϱ), δ=exp(gδ), matching Eq. 3.18. These three draws are illustrative, not inferred parameters; no colors are extracted as data from hero.png. The diagram does not interpolate or imply a fitted spatial surface. The expanded explanation distinguishes local marginals from the hierarchical dependence model.

## Numerical results

25 configurations: all nine ξ∈{−1,0,+1}, δ∈{0,1,3} reference cases, shapes ±10⁻⁹, −0.5 and −1.5, three spatial sites, and a small positive δ with nonzero μ and nonunit ϱ.

- Exact δ=0 GEV reduction; correct point values at μ and ξ=−1 endpoints.
- Monotone CDF on 1,001 ordered points per configuration, and limits exactly 0/1 at infinity.
- Adaptive Simpson integration split at quantiles and μ: maximum error from 1 was 1.733×10⁻⁷ (acceptance 2×10⁻⁶). Bounds are Q(10⁻¹⁰) and Q(1−10⁻¹⁰), so omitted probability is 2×10⁻¹⁰; this validates the distribution across its tails, not just the graph window.
- Interior central-difference derivative (step 10⁻⁶): maximum absolute error 8.731×10⁻¹¹ (acceptance 2×10⁻⁷).
- F(Q(p)): maximum absolute error 1.426×10⁻¹¹ (acceptance 2×10⁻⁸), including tail probabilities 10⁻¹⁰ and 1−10⁻¹⁰.
- Separate near-zero ξ checks at ±10⁻¹⁰; endpoint limits and the intentional discontinuous pointwise δ change at μ.
- All three original PDFs rendered and visually inspected. Independent vector-coordinate comparison samples 300 points from each of 18 paths (density and CDF for the nine presets). Maximum residual 0.306 PDF points, within propagated coordinate-rounding tolerance: x uncertainty 0.0007 data units plus 0.035 vertical PDF points. Points near the ξ=−1 support jump are excluded from vector comparison and verified analytically instead. Fixtures are extracted using `compare-reference-pdfs.py ORIGINAL_FIGURE_DIRECTORY` (requires pypdf); PDFs are never modified.

## Visual and interaction review

Browser review at 1440×1000 and 390×844, including the Jacobian intermediate state, shape endpoints and spatial sites. Corrected the mobile SVG viewBox and equation spacing. Verified all nine presets, manual pause, progress seeking, site selection, keyboard delta increment/decrement, no NaN/Infinity in rendered paths, no horizontal page overflow and no browser console errors. Static SVG fallback inspected separately.

`prefers-reduced-motion` starts paused and removes editorial transitions; Play remains an explicit opt-in. Media-query changes pause playback. IntersectionObserver suspends the story clock outside the viewport; hidden documents also suspend it. These lifecycle guards were inspected in code; OS-level reduced-motion emulation was not available in the review browser.

## Limits

Stable x window [−4,8]; the displayed outside probability is computed from the exact CDF. The ξ=1, δ=0 heavy tail extends well beyond this window (about 10.52% omitted), explicitly reported and never renormalized. Density y maximum is fixed at 1.8 for the movie and ξ=0/+1 presets, and 4.3 for ξ=−1, preserving the height-4 endpoint. Curves are sampled at 1,001 points plus μ and finite support endpoints; this is a lightweight numerical plot, not a proof or a general-purpose plotter for arbitrary parameters. Very small positive δ forms a narrow notch at μ that no finite screen can fully resolve. Spatial scenes switch between discrete locations rather than implying a probabilistic transformation between sites. The full mathematical details are available through the disclosure below the controls.
