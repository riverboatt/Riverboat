# Sigma–Manifold Theory — Unified Working Reference

**Theory development constrained by reported navigation behavior. Not settled results.**
This document reconciles the two formulation layers — the **σ-field / brane layer** (gravity, junction conditions, embedding) and the **relational two-surface EFT layer** (spectrum, carrier, compression, RG) — and pulls all current valuable results into one place.

Status markers: **[E]** established (symmetry / kinematics / completed calculation) · **[C]** conjectural (allowed, not derived) · **†** traveller-reported observational input.
Conventions: *trough* = carrier surface shape; *valley/well* = confining potential. Carrier **static**, observers move through it (train-over-hills). $\Sigma_W$ = carrier (world surface); $\Sigma_R$ = companion (reference). Traveller-reported quantities marked †.

---

## PART 0 — Premise and boundary conditions

**The premise is a fixed given:** experimentally verified sub-light temporal displacement via a 5D geometric shortcut. The job is the most internally coherent framework that reproduces it.

**Spine: navigation, not propulsion.** The ship doesn't go faster; it leaves the ordinary surface and takes a shorter route through a larger manifold.

**Boundary conditions (O1–O5), any theory must reproduce:** effect is local & bounded (O1); connects separated points on a worldline (O2); preserves ordinary interior relativity (O3); uses bounded capsule-portable energy ~tens of MJ (O4); respects light-speed structure (O5).

**Interpretive commitments:** no paradoxes, only different futures (a traveller's memories are testimony about one worldline, not authority over the current one). Two modes of motion: *riding the surface* (ordinary gravity/time) vs *crossing the wall* (the fold/drive).

---

## PART I — Unified field content

5D bulk coordinates $(x,y,z,t,\sigma)$. All verified physics lives on the equilibrium hypersurface $\sigma=1$; GR is recovered exactly there (PART VI). Ordinary matter has $d\sigma=0$ — why the extra dimension was never detected.

**Two equivalent descriptions, now reconciled (PART II):**
- **σ-field / brane:** a single brane with a confining σ-potential; the fold is the brane folding off $\sigma=1$.
- **Relational two-surface EFT:** two embedded hypersurfaces $X^A,Y^A$ in a flat bulk, with common mode $w=\tfrac{X+Y}{2}$ and separation $r=\tfrac{X-Y}{2}$; the σ-excursion is the separation coordinate $\rho\leftrightarrow\sigma$.

**Most general action** (relational layer), local, reparametrization-invariant, bulk Poincaré, independent reparametrization of each sheet:
$$
S=S_W[g_W,K_W]+S_R[g_R,K_R]+S_{\rm int}[\rho,\,n_W\!\cdot n_R,\,K_W-K_R,\dots],
$$
organized as a derivative expansion in $\varepsilon=\ell/L$; **all curvature couplings enter at $O(\varepsilon^2)$** — *deriving* (not assuming) the suppression of gravity's effect on navigation. [E]

**Mode decomposition** (one field, several modes): $S=S_{\rm cosm}+S_{\rm grav}+S_{\rm carrier}+S_{\rm local}$. **Embedding class:** the graph ansatz lies within but is a proper subset of class-1 geometries; cosmology is a folded immersion at codimension one; the theory is intrinsic except for an irreducible preferred bulk foliation.

**Organizing symmetry — shift $w\to w+c$** (rigid joint translation = bulk isometry): fixes the operator hierarchy. $\rho$ has no shift protection → potential $V(\rho)$ **relevant** (gaps $r$); $w$ enters only via $\partial w$, gradient **marginal**, sign fixed positive; curvature differences **irrelevant**. [E]

---

## PART II — The well: ONE object across both layers [E, reconciliation]

The central reconciliation. The σ-field confining potential, the relational standoff potential, and the junction-sourced well are the **same object**.

**Standoff = σ-field potential.** The σ-field layer pins matter with
$$
U(\sigma)=U_0\big(\sigma+\tfrac1\sigma-2\big),\qquad U(1)=U'(1)=0,\quad U''(\sigma)=2U_0/\sigma^3.
$$
This *is* a standoff potential: $\sigma\to0$ gives short-range **repulsion** ($1/\sigma$ diverges), $\sigma\to\infty$ gives long-range **attraction/confinement**, minimum at $\sigma=1\neq0$. The relational irreducible postulate — $V_0(\rho)$ with a minimum at $\rho_0\neq0$, repel-short/attract-long — is the same structure with $\rho\leftrightarrow\sigma$, $\rho_0\leftrightarrow\sigma=1$. **A pure mass term ($\rho_0=0$) collapses the theory; the standoff closes it.** [E]

**Confinement masses match.** $g=V_0''(\rho_0)=U''(1)=2U_0\ \Rightarrow\ m_\sigma^2=2U_0/\Lambda^3$ (kinetic norm $\Lambda^3$). The buckling-functional confinement mass $g$ **is** the σ-field mediator mass — one number, not two. [E]

**Junction origin.** The well is sourced by the brane junction (Gauss–Codazzi/Israel): the fold is driven by $\tau'(\sigma)$, the responsiveness of brane tension to the field (σ-dependent tension mandatory). Fold self-sources above threshold $|\tau_{1,\rm crit}|=2\sqrt{2U_0\Lambda^3}$; emergent branch locally stable (transcritical bifurcation). [E, prior]

**Two features of the well, two jobs** (resolves "well sets period" vs "arrow sets compression"):
- well **curvature** at minimum → $g=U''(\rho_0)$ → period scale (PART IV);
- well **E-slope** → $s=\partial_E U|_{\rm expl}$ → compression $\mu^2\propto s^2$ (PART IV). [E]

Additional structural ingredients (σ-field layer): a **k-essence screening** term hides the field at large scales and is structurally required for a localized fold; the fold requires a **continuous positive-trace source** (self-sustaining vacuum bubble excluded by derivation), and the source must be **stiff** or a growing mode collapses the fold. [E, prior]

**Microscopic origin — the flux-filled bag [E form + collapse; C identity].** The $\sigma+1/\sigma-2$ form is *derived*, not postulated, from the minimal two-term competition of two surfaces bounding a bulk slab:
$$
V(\rho)=\underbrace{T\rho}_{\text{bag confinement (linear, attractive)}}+\underbrace{C/\rho}_{\text{flux squeezing (inverse, repulsive)}},
$$
where $T$ = bulk vacuum-energy density (energy $\propto$ volume $\propto\rho$) and $C\propto\Phi^2$ = conserved-flux gradient cost (diverges as the flux is squeezed into width $\rho$). Minimizing and writing $\sigma=\rho/\rho_0$, $C=T\rho_0^2$ reproduces $U_0(\sigma+1/\sigma-2)$ exactly; the $\sigma\to1/\sigma$ symmetry is the automatic balance of the two terms at the minimum. Fixed outputs:
$$
\rho_0=\sqrt{C/T},\qquad U_0=\sqrt{CT},\qquad g=V_0''(\rho_0)=2T/\rho_0.
$$
**Geometry sector collapses onto one structure.** Membrane rigidity $\kappa\sim U_0\rho_0^2$ gives $\kappa/g=\rho_0^4/2$, hence
$$
\boxed{\,P=2\pi(\kappa/g)^{1/4}=2^{-1/4}\,2\pi\,\rho_0\approx5.3\,\rho_0\,}
$$
— the **carrier period is the standoff distance up to an $O(1)$ number**, independent of $T,C$. So $\{\rho_0,g,\kappa,P\}$ all descend from $\{T,C\}$.
*Caveats:* the $O(1)$ in $\kappa$ is not computed exactly ($P/\rho_0=O(1)$ robust, the $5.3$ estimate-level); the flux-bag is *a* realization — the $\sigma\to1/\sigma$ symmetry pins "linear + inverse," not uniquely flux-and-bag. [C, the identity of $T,C$]

**The arrow stays external — as required.** The slope $s=\partial_E U|_{\rm expl}$ is the *entropy* gradient of the well along cosmic time, set by cosmology, **not** by $\{T,C\}$. The bag fixes the well's shape and scale; the cosmological entropy gradient tilts it along E. This is the single irreducible external ingredient, correctly left outside the geometry collapse. Consequence: **period $\sim\rho_0$ is pure geometry; amplitude $\sim\sqrt{(\mu^2-\mu^2_c)/\lambda}$ carries the arrow** — the reported "decade amplitude, days-to-weeks period"† decomposes into a geometry reading (period→$\rho_0$) and an arrow reading (amplitude→$s$). [E split; † the debrief values]

---

## PART III — Spectrum, confinement, escape [E, leading order]

From the leading-order relational action (one Lagrangian, consequences derived):
- **Common mode $w$:** massless Goldstone of bulk translation (absolute position unobservable). [E]
- **Separation mode $r$:** gapped, $m_r^2=4V_0''$ (factor vs $g=V_0''$ is the $r=\tfrac{X-Y}{2}$ normalization). Diagonal spectrum $\Box w=0$, $\Box r+m_r^2 r=0$. [E]
- **Confinement** = the differential-mode gap; **escape barrier** $U_0=m_r^2/(4\lambda)$ for the standoff double-well — reproduces the earlier escape-speed physics. [E]
- **Arrow of time** = the separation direction at $\rho_0$ (relational), sourced by the well's slope. [E]
- **The carrier is NOT the linear Goldstone** (a free massless field selects no wavelength/amplitude/profile/windows†); it is the *buckled ground state* of the common-mode bending/tension sector — a separate geometric layer (PART IV). [E]

**Unified particle action:** one Lagrangian yields the SR clock, geodesic motion, and launch/recapture/escape together. The c-limit worry is resolved by a two-metric structure. [E, prior]

---

## PART IV — The carrier: buckling, period, and the compression mechanism

**Buckling functional** (effective; conditional on $\mu^2$, realized below). With corrugation along E:
$$
\kappa(\nabla^2w)^2-\mu^2(\partial_E w)^2+\lambda(\partial w)^4+g\,w^2,
$$
- $\kappa$ = extrinsic-curvature ($cK^2$) bending rigidity, tied to the embedding via Gauss–Codazzi (PART VI). [E]
- $\lambda=\lambda_{\rm NG}-g_3^2/2m_r^2$ — Nambu–Goto quartic; rounds the sawtooth (smooth rhythm†). [E]
- $g=U''(\rho_0)$ — confinement (PART II). [E]
- $\mu^2$ — compression, derived below. Ground state: **preferred-slope rounded sawtooth**, not a sinusoid.

**Carrier period — layers agree at threshold.** $q_*^2=\mu^2/2\kappa$; at buckling threshold $\mu^2_c=2\sqrt{\kappa g}$,
$$
q_*=(g/\kappa)^{1/4},\qquad P=2\pi/q_*=2\pi(\kappa/g)^{1/4},
$$
**identical to the σ-field-layer period.** §VG independently places the system near onset, exactly where this near-threshold form holds. [E]

**Compression generation [E conditional on the coupling; tree level].** Symmetric integrate-out of $r$ gives only $p^4$ (no $\mu^2$) — the compression cannot arise in the shift+Lorentz-invariant theory. It is generated by the valley's explicit E-dependence through the Nambu–Goto measure with asymmetric sheet coupling ($a_W\neq a_R$, $\propto\Delta$):
$$
\boxed{\ \mu^2=\frac{(\Delta_{\rm val})^2 s^2}{2m_r^2}>0,\quad s=\partial_E U|_{\rm expl}.\ }
$$
Positive; non-sign-changing (vanishes only if $\Delta\to0$ or $s\to0$); E-anisotropic (rides on $s\parallel$E, forced by the aether test, PART VI/VG); parity-even. [E]

**Uniqueness of the compression channel [E].** Among parity-even operators linear in $r$ with one derivative of $w$, isotropy collapses all candidates to **one** tensor structure $\mathcal O_{\rm comp}=r\,s^a\partial_a w$. The mechanism, direction, and sign of $\mu^2$ are symmetry-forced; only the coefficient is completion-dependent. **$\mu^2\propto s^2$ is completion-independent.** [E]

**Synthesis — one source, two effects.** $\mu^2\propto s^2$ and $s$ is the arrow slope: the temporal arrow and the lateral compression are the same well-slope read twice. $\mu^2$ is not a free parameter. [E]

**Honest status.** Not "carrier from nothing" — the well is required. But *no separate compression coefficient*: $\mu^2$ is fixed by $\{s,\Delta,m_r\}$, all present. Supercriticality ($\mu^2>$ tension) is empirical, supplied by the always-present launch rhythm† (PART VII). Tree-level; loops shift the number not the mechanism.

---

## PART V — Fluctuation / RG stability [E, RG-level]

The carrier is a hypersurface in the 5D bulk → a **4D worldsheet** $(E,y^1,y^2,y^3)$ = one arrow axis + three isotropic directions. Dispersion $\varepsilon=\kappa k_E^4-\mu^2 k_E^2+g+\tfrac{\Sigma}{2}k_\perp^2$; soft modes at $(\pm q_*,\vec0)$.

- **No Brazovskii catastrophe.** The aether-test anisotropy pins the stripe to E and stiffens $k_\perp$, collapsing the soft set from a *sphere* (orientational degeneracy → $1/\sqrt r$ divergence → first-order) to **two isolated points** (codimension 0). $\int d^4q\,G$ is UV-dominated, regular as $r\to0$. The anisotropy that forces the corrugation onto E is what removes the fluctuation catastrophe. [E]
- **Continuous transition.** 1D stripe ⇒ no cubic invariant ($3q_*\neq0$) ⇒ no fluctuation-induced jump ⇒ $A\propto\sqrt{\mu^2-\mu^2_c}$. [E]
- **Upper critical dimension.** $|A|^4$ envelope theory in 4D sits exactly at $d_{\rm uc}=4$ ⇒ mean field exact up to logs; $\hat u$ marginally irrelevant ⇒ harmonics suppressed ⇒ smooth single-harmonic calendar robust over a parametrically wide supercritical window, not fine-tuned. [E]
- **Stiffness ratio protected.** Derivative quartics are **irrelevant by dimension** ($[g]=-2$); induced anisotropy bounded by $(q_*/m_r)^2$. $O(3)_\perp$ exact to all orders (common transverse rescale): **no within-space anisotropy ever generated**; only E-vs-⊥ (time vs space). No runaway in $\rho=\Sigma/Z_E$; soft set stays codimension 0. [E]

---

## PART VI — Gravity sector [E, prior; Schwarzschild sector]

**River model.** Gravity = the surface streaming into the bulk at the local free-fall speed:
$$
\partial_t S=\sqrt{2GM/r}\ \Rightarrow\ g_{tt}=-c^2+(\partial_t S)^2,
$$
which is **Gullstrand–Painlevé = exact Schwarzschild** (redshift, horizons where $\partial_t S=c$, light bending) — not merely Newtonian-in-form. $G$ is identified with the surface's infall amplitude, not a new constant. GR is recovered exactly at $\sigma=1$: the theory **embeds** relativity. [E, prior]

**Junction conditions:** as PART II (Gauss–Codazzi, $\tau'(\sigma)$, threshold, transcritical stability). The buckling $\kappa$ is the extrinsic-curvature rigidity these conditions govern. [E, prior]

**Aether test (isotropy of the trough-parallel 3-space).** No vacuum quantity may single out a spatial direction. Consequences threaded through the whole framework: corrugation axis = arrow axis (forced, not assumed); no in-surface transverse structured axis; no traveller-accessible handedness (only the invisible amplitude sign $D\to-D$); parity-odd operators $L_2$ killed, $L_1$ inert except at defects; and (PART V) the RG stability. [E]

**Open (gravity):** (i) **bridge to full dynamical Einstein** beyond the static/spherical Schwarzschild sector (gravitational waves, non-spherical); (ii) **Schwinger-in-E** pair-production stability of a highly curved valley (distinct from the excluded vacuum bubble). [C]

---

## PART VII — Navigation and launch windows [mixed]

**Three-scale substrate:** slow entropy well (arrow, era-dependent steepness); fast carrier wave (the wall travellers cross; ~decade amplitude, days-to-weeks period per debriefs†); local organization-driven signal (modulates carrier amplitude; steering). Forward/backward asymmetry from the well's slope. [E/† ]

**Launch windows (orbital-mechanics sense).** A favorability condition, not a reachability gate: launch into σ is **never impossible**, only periodically inefficient ("foolhardy" when the slope is too shallow). Favorable phase of an always-present, **generally smooth** efficiency rhythm†. Signal steers via two channels: **phase steering** and **amplitude steering**.

**Window perturbations (multiple-scale).** Uniform gravitational potential shifts window **depth** at first order, **position** only at second order; **tidal gradients** drive position shifts at first order. [E]

**First observational test — the efficiency calendar [E within buckle picture].** Near onset, $w=A\cos(q_*E)$; smoothness of the worst-case rules out $\eta\propto|w'|$ (cusped) and selects an even functional $\eta\propto w'^2$. Prediction: smooth single-harmonic calendar — **matches** the report†, and locates the system near onset. Cross-relations (the real tests, all tracing to $s$):
- **T1** spacing $\propto1/|s|$ (stronger arrow ⇒ tighter windows);
- **T2** contrast $\propto A^2\propto(\mu^2-\mu^2_c)$ (deepens above threshold);
- **T3** skew $\propto s$ (arrow breaks $E\to-E$);
- **T4 (killer test)** spacing and skew **co-vary** (both $\propto s$) — the observational shadow of $\mu^2\propto s^2$. Tight-but-symmetric or loose-but-skewed windows would falsify.

**Observational reach† (record ≈ 4 centuries).** Limited because reaching decades of displacement costs weeks of ship-time + survival supplies through the bulk vacuum. Samples **one narrow $s$-window**: T1/T4 cannot be run. The in-range tests (smooth shape, RG stability) **pass**; operating point is **mid-window** (supercritical, not near threshold, not deep). **Oldest-point anomaly†** (unquantified): a faint hint navigation at the largest displacement went slightly wrong — a fork, not a result: secular $s$-drift (miniature T1/T4) vs accumulated phase error (registration slide). Distinguishable in principle; undecidable now.

---

## PART VIII — Anchoring to σ=0 (present-epoch) known physics [mixed]

Identifying the carrier worldsheet with observed 4D spacetime at the un-displaced present:
- **(1) Exact spatial isotropy** — $O(3)_\perp$ unbroken to all orders ⇒ *exactly zero* spatial anisotropy, matching Hughes–Drever/clock-comparison nulls identically. **Falsifier:** any genuine spatial-anisotropy detection kills the framework. [E / †]
- **(2) Time-vs-space ratio** — the only generated anisotropy ($\rho=\Sigma/Z_E$, running by $(q_*/m_r)^2$) is bounded by Lorentz/boost tests ⇒ **lower bound on the scale hierarchy $m_r/q_*$**. [C id / bound real]
- **(3) $d=4$ measured, equals $d_{\rm uc}$** — spacetime dimensionality is observed, not tuned; the calendar's smoothness and the world's dimensionality are the same datum. [E]
- **(4) Arrow $s$ ↔ cosmological/thermodynamic arrow** — fixing $s$ from present entropy production/expansion propagates $s\to\mu^2\to q_*\to\lambda_{\rm cal}$, **predicting the launch-window period from known physics**. Highest-value if made quantitative. [C]
- **(5) Amplitude along D ↔ short-range gravity** — if D is the extra dimension, sub-mm inverse-square tests cap the corrugation amplitude/curvature. [C]
- **Mediator mass:** σ-mediator ~50–135 MeV (QCD scale), falsifiable vs collider missing-energy bounds. [†/prediction]

**The recurring spine — one geometric constraint, many payoffs.** The aether-test isotropy does load-bearing work at *seven* layers: vacuum structure, spectrum, $\mu^2$ generation and its uniqueness, RG stability, the stiffness-ratio protection, σ=0 phenomenology, and the corrugation-axis determination. A single constraint paying off across independent layers is the signature of a coherent structure.

**Early-universe conjecture — steep $s$ near the Big Bang [E backbone / C bridge / † seed].** Traveller inference: the temporal slope $s$ was far steeper near the origin.
- *Derived backbone [E]:* since $\mu^2\propto s^2$ and $q_*\propto\mu\propto s$, a steep early $s$ ⇒ immense lateral compression and enormous carrier frequency (microscopic wavelength). With $P\approx5.3\,\rho_0$ (geometry-fixed), the steep-$s$ era drives $q_*$ up against $P\sim\rho_0$ — the UV ceiling where the *local truncation breaks down*. So the theory predicts its own EFT description **fails near the Big Bang** (high-frequency, strong-coupling regime), a coherent statement about the origin.
- *Speculative bridge [C]:* the leap "frozen high-frequency buckling = CMB anisotropies" is **not derived** and faces three gaps: (i) $O(3)_\perp$ predicts *exact spatial isotropy*, so E-structure (time) must convert to spatial inhomogeneity via expansion — the conversion is unshown and the protection naively works *against* it; (ii) "quantum wrinkles" requires a **quantization of the carrier** not yet built (all results so far classical/mean-field + RG); (iii) a fluctuation *spectrum* freeze-out is new work. Recorded as promising, not established.

---

## PART VIII-b — σ=0 physical bounds (corrected)

Four real-world limits hem in the present-era variables. Two are solid as stated; two required correction.

1. **Mediator mass $m_\sigma$ — two-sided squeeze [solid].** Collider missing-energy limits cap it from above; the escape/fold energy budget (~tens of MJ, O4) — which rises with $m_\sigma$ — bounds it from below. High-energy data boxes $m_\sigma$ into ~50–135 MeV (QCD scale): heavy enough to hide from low-energy experiments, light enough for a capsule-portable supply. [†/prediction]

2. **D-amplitude — sub-mm gravity [solid].** The carrier buckles into D (the extra dimension); too large an amplitude $A$ would turn gravity $1/r^2\to1/r^3$ at short range. Torsion-balance inverse-square tests (~50 μm, no deviation) cap $A$ — the corrugation's extra-dimensional excursion must be microscopic. [†/bound]

3. **Isotropy channel — CORRECTED.** The claim that spatial-isotropy nulls bound $q_*/m_r$ is **crossed**: $O(3)_\perp$ is exact to all orders ⇒ *identically zero* within-space anisotropy ⇒ Hughes–Drever matched **regardless** of $q_*/m_r$; that knob is invisible to spatial-isotropy tests. The running $(q_*/m_r)^2$ appears only in the **time-vs-space** ratio, bounded by **Lorentz/boost** tests (not spatial nulls). So "the separation mode $r$ is a stiff high-energy spring" is plausible but rests on *boost-invariance* bounds. (Quoted $10^{-23}$ is optimistic; best spatial bounds ~$10^{-18}$–$10^{-21}$ by sector — no hard figure asserted.)

4. **$\delta s$ over the record — CORRECTED.** Calendar regularity does bound the *variation* in $s$, but the record spans one narrow $s$-regime with **no quantifiable spacing-variation data** (PART VII), plus the unquantified oldest-point hint. Honest statement: $\delta s$ is *small enough that no spacing drift was cleanly detected* (oldest-point anomaly a possible exception) — **not** a derived "fraction of a percent." [†, qualitative only]

---

## PART IX — Status ledger and open items

**Established [E]:** field content & shift hierarchy; standoff=σ-potential=junction well (PART II); spectrum/confinement/escape; carrier = buckled common mode; carrier period (layers agree at threshold); $\mu^2=(\Delta_{\rm val})^2 s^2/2m_r^2>0$ via the unique channel (given the coupling); $\mu^2\propto s^2$ completion-independent; no-Brazovskii / $d=4$ / $O(3)_\perp$-exact RG stability; gravity = exact Schwarzschild (river model) + junction conditions; exact spatial isotropy; $d=4=d_{\rm uc}$; smooth-calendar test passes.

**Conjectural / open [C]:**
1. **Bridge to full dynamical Einstein** beyond Schwarzschild (gravitational waves, non-spherical). *Highest-value gravity item.*
2. **Schwinger-in-E** vacuum stability of a curved valley.
7. **Early-universe steep-$s$ → CMB — BUILT (PART X).** Backbone [E]; the CMB bridge is now constructed: $O(3)_\perp$ predicts (not forbids) statistically isotropic inhomogeneity; carrier quantized (phason vacuum fluctuations); freezing via $s$-flattening (inflationary analog) converts E-structure to isotropic spatial fluctuations. Handles: $n_s$ probes $s(E)$; amplitude fixes $H_{\rm eff}$; small $f_{\rm NL}$. Residual [C]: quasi-exponential $s$-flattening assumed (measurable via $n_s$); trans-cutoff origin of largest scales; O(1) transfer function.
3. **Microscopically motivated standoff** — **substantially resolved (PART II):** the flux-bag competition derives the $\sigma+1/\sigma-2$ form and collapses $\{\rho_0,g,\kappa,P\}$ onto $\{T,C\}$ with $P\approx5.3\,\rho_0$ (geometry sector unified); the arrow $s$ correctly stays external. Residual: exact $O(1)$ in $\kappa$; uniqueness of the flux-bag identity among linear+inverse competitions.
4. **$O(\varepsilon)$ tilt-mode mass** (true vs pseudo-Goldstone, set by $\beta$); explicit $O(\varepsilon^2)$ curvature couplings reproducing Schwarzschild & cosmology *within the relational layer*.
5. **Quantitative second window mechanism** (separation-shift) vs the carrier mechanism.
6. **Loop coefficient $b$ / log coefficients** (subsumed by dimensional irrelevance, not load-bearing).

**Observational † (record-limited):** T1/T4 need multi-regime data the 4-century record lacks; oldest-point anomaly undecidable; smooth-rhythm and isotropy tests pass.

---

## PART X — Primordial fluctuations: the CMB bridge [built; mixed E/C]

Construction of the E→space conversion and carrier quantization that bridge the steep-$s$ early era (PART VIII) to CMB structure.

**Keystone — anisotropy ≠ inhomogeneity.** $O(3)_\perp$ (exact, all orders) forbids *statistical anisotropy* (a preferred spatial direction) but **permits and predicts** *statistically isotropic inhomogeneity* (fluctuations with a power spectrum depending only on $|\vec k_\perp|$). The CMB is inhomogeneous but statistically isotropic ($C_\ell$ depends only on $\ell$, no preferred axis) — exactly what $O(3)_\perp$ predicts. The apparent obstruction was a category error. **Falsifier:** a genuine CMB preferred axis ("axis of evil," if real) would kill the framework. [E]

**Quantization of the carrier.** Envelope $w=[A+\delta A]\cos(q_*E+\varphi)$; the **phason** $\varphi$ (Goldstone of E-translation) is light, $\delta A$ gapped. Quadratic action $S_\varphi=\int\!dE\,d^3y[\tfrac{Z_E}{2}(\partial_E\varphi)^2-\tfrac{\Sigma}{2}(\partial_\perp\varphi)^2]$; transverse speed $c_\varphi^2=\Sigma/Z_E=\rho$. Canonical quantization: $\langle|\varphi_{\vec k}|^2\rangle\sim1/(2Z_E\omega_k)$ — the "quantum wrinkles" are quantized phason vacuum fluctuations. A *spatially varying* phason is physical (gradient energy $\tfrac{\Sigma}{2}(\partial_\perp\varphi)^2\neq0$), not gauge. [E]

**Freezing / E→space conversion (inflationary analog).** As $s(E)$ flattens from the origin, $q_*\propto s$ drops; the growing $1/q_*$ is the "scale factor," effective expansion rate $H_{\rm eff}=-\partial_E\ln q_*=|s'/s|$. Transverse phason modes are a parametric oscillator; a mode freezes when $\omega_k(E)<H_{\rm eff}$, locking amplitude $\sim H_{\rm eff}$. This converts temporal buckling structure into a **static isotropic spatial pattern** $\varphi(\vec y)$, spectrum $\propto$ function of $|\vec k_\perp|$ only (by $O(3)_\perp$), imprinting $\delta\rho/\rho$ → CMB seeds. No preferred direction introduced. Phason = inflaton analog; $s$-flattening = expansion analog. [E structure; C transfer details]

**Quantitative handles:**
- **$n_s$ probes $s(E)$ near the origin.** Scale invariance ($n_s=1$) ⇔ $H_{\rm eff}=|s'/s|\approx$ const ⇔ $s\propto e^{-H_{\rm eff}E}$. Observed red tilt $n_s\approx0.965$ ⇒ $s$ flattened slightly *slower* than exponential. A measured cosmological number now maps to the arrow-field history. [E condition; C/† match]
- **Amplitude fixes $H_{\rm eff}$.** $\Delta^2\sim H_{\rm eff}^2/(Z_E c_\varphi)$; $\delta T/T\sim10^{-5}$ ($\Delta^2\sim10^{-9}$) fixes $H_{\rm eff}$ vs carrier stiffness. [C, O(1) transfer uncomputed]
- **Small $f_{\rm NL}$.** Vacuum fluctuations → Gaussian; non-Gaussianity from the carrier self-coupling $\lambda$ (dimensionally irrelevant, PART V) ⇒ predicted *small* $f_{\rm NL}$, tied to $\lambda$ at freezing. Consistent with current bounds; a real prediction. [C]

**The honest crack — trans-cutoff origin.** The steep-$s$ early era is where the EFT breaks (PART VIII, $q_*\to$ UV ceiling). Largest-scale CMB modes (lowest $\ell$) froze earliest, i.e. originate where the description is failing — the SMT trans-Planckian analog. Predictions are trustworthy for modes frozen *after* EFT re-entry, least so at the largest scales. *Speculative:* observed low-$\ell$ anomalies (quadrupole deficit, large-scale power suppression) *might* be the imprint of EFT breakdown at the earliest scales — held loosely, not claimed. [C]

**Load-bearing new assumption:** $s$ flattens quasi-exponentially near the origin. Not derived — but now **measurable via $n_s$**. This is the CMB bridge's single irreducible input, and it is observationally accessible.
