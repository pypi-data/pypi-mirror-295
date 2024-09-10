/-
This is a d∃∀duction file providing exercises for sets and maps. French version.
-/

-- Lean standard imports
import tactic
-- import data.real.basic


-- dEAduction tactics and theorems
-- structures2 and utils are vital
import structures2      -- hypo_analysis, targets_analysis
import utils            -- no_meta_vars
import push_neg_once    -- pushing negation just one step
-- import induction     -- theorem for the induction proof method
-- import compute_all   -- tactics for the compute buttons

-- dEAduction definitions
import set_definitions

-- Use classical logic
local attribute [instance] classical.prop_decidable

-------------------------
-- dEAduction METADATA --
-------------------------
/- dEAduction
Title
    Ensembles et applications
Description
    Deux exercices de théorie des ensembles utilisant l'injectivité.
AvailableProof
    proof_methods new_object
AvailableCompute
    NONE
AvailableExercises
  UNTIL_NOW -image_directe_et_inclusion_II -image_reciproque_et_inclusion_II -image_directe_et_intersection_II
  -image_de_image_reciproque_I -image_reciproque_de_image_II
  -injective_si_compo_injective_I -surjective_si_compo_surjective_II
  -image_directe_et_intersection_VI
AvailableDefinitions
  UNTIL_NOW -singleton -paire -identite -egalite_fonctions
AvailableTheorems
  UNTIL_NOW -image_singleton -image_paire
Settings
    functionality.allow_induction --> false
    functionality.calculator_available --> true
-/

---------------------------------------------
-- global parameters = implicit variables --
---------------------------------------------
section course
variables {X Y Z: Type}


open set

------------------
-- COURSE TITLE --
------------------
namespace ensembles_et_applications
/- dEAduction
PrettyName
    Ensembles et applications
-/

namespace logique

lemma definition.iff {P Q : Prop} : (P ↔ Q) ↔ ((P → Q) ∧ (Q → P)) :=
/- dEAduction
PrettyName
    Equivalence logique
-/
begin
  exact iff_def,
end

lemma theorem.disjonction_eqv_implication (P Q: Prop) :
(P ∨ Q) ↔ ((not P) → Q)
:= 
/- dEAduction
PrettyName
    Disjonction sous forme d'implication
-/
begin
  tautology,
end

end logique

namespace definitions
/- dEAduction
PrettyName
    Définitions
-/
namespace generalites

/- dEAduction
PrettyName
    Généralités
-/

lemma definition.inclusion {A B : set X} : A ⊆ B ↔ ∀ {x:X}, x ∈ A → x ∈ B :=
/- dEAduction
ImplicitUse
  True
-/
begin
    exact iff.rfl
end

lemma auxiliary_definition.negation_egalite_ensembles {A A' : set X} :
(A ≠ A') ↔ ¬ ( ∀ x, x ∈ A ↔ x ∈ A' ) :=
begin
    todo
end


lemma definition.egalite_ensembles {A A' : set X} :
(A = A') ↔ ( ∀ x, x ∈ A ↔ x ∈ A' ) :=
/- dEAduction
PrettyName
    Egalité de deux ensembles
AuxiliaryDefinitions
  auxiliary_definition.negation_egalite_ensembles
-/
begin
     exact set.ext_iff
end

lemma auxiliary_definition.negation_double_inclusion {A A' : set X} :
A ≠ A' ↔ ¬ (A ⊆ A' ∧ A' ⊆ A) :=
begin
    todo
end

-- Unfortunately split cannot work
lemma definition.double_inclusion {A A' : set X} :
A = A' ↔ (A ⊆ A' ∧ A' ⊆ A) :=
/- dEAduction
PrettyName
    Double inclusion
ImplicitUse
  True
AuxiliaryDefinitions
  auxiliary_definition.negation_double_inclusion
-/
begin
    exact set.subset.antisymm_iff
end

lemma definition.ensemble_vide
{A: set X} :
(A = ∅) ↔ ∀ x : X, x ∉ A
:=
begin
    exact eq_empty_iff_forall_not_mem,
end

lemma auxiliary_definition.ensemble_non_vide
(A: set X) :
(not (A = ∅) ) ↔ ∃ x : X, x ∈ A
:=
begin
    todo
end

lemma definition.ensemble_non_vide
(A: set X) :
(A ≠ ∅) ↔ ∃ x : X, x ∈ A
:=
/- dEAduction
AuxiliaryDefinitions
  auxiliary_definition.ensemble_non_vide
ImplicitUse
  True
-/
begin
    todo
end



lemma definition.singleton
{x x_0: X} :
(x ∈ ((singleton x_0): (set X))) ↔ x=x_0
:=
begin
    refl,
end

lemma definition.paire
{x x_0 x_1: X} :
(x ∈ ((pair x_0 x_1): set X)) ↔ (x=x_0 ∨ x=x_1)
:=
begin
    refl,
end

end generalites

---------------
-- SECTION 1 --
---------------
namespace unions_et_intersections
-- variables unions_et_intersections --
variables {A B C : set X}

lemma definition.intersection_deux_ensembles {A B : set X} {x : X} :
x ∈ A ∩ B ↔ ( x ∈ A ∧ x ∈ B) :=
/- dEAduction
PrettyName
    Intersection de deux ensembles
ImplicitUse
    True
-/
begin
    exact iff.rfl
end

lemma definition.union_deux_ensembles  {A : set X} {B : set X} {x : X} :
x ∈ A ∪ B ↔ ( x ∈ A ∨ x ∈ B) :=
/- dEAduction
PrettyName
    Union de deux ensembles
ImplicitUse
    True
-/
begin
    exact iff.rfl
end

end unions_et_intersections


namespace applications

-- variables applications --

variables  {A A': set X}
variables {f: X → Y} {B B': set Y}

lemma definition.egalite_fonctions {f' : X → Y} :
f = f' ↔ ∀ x, f x = f' x :=
/- dEAduction
PrettyName
    Egalité de deux fonctions
-/
begin
    exact function.funext_iff,
end


lemma definition.identite {f₀: X → X} :
f₀ = Identite ↔ ∀ x, f₀ x = x :=
/- dEAduction
PrettyName
    Application identité
-/
begin
    apply definition.egalite_fonctions,
end


lemma definition.image_directe {y : Y} :
y ∈ f '' A ↔ ∃ x : X, x ∈ A ∧  f x = y
:=
begin
    refl,
end

lemma exercise.image_directe :
∀ f: X→Y, ∀{A: set X}, ∀{x: X},
 (x ∈ A → f x ∈ f '' A)
:=
begin
    todo
end

lemma definition.image_reciproque {x:X} :
x ∈ f  ⁻¹' B ↔ f(x) ∈ B
:=
begin
    refl,
end

variables (g : Y → Z)

lemma definition.composition {x:X}:
function.comp g f x = g (f x)
:=
begin
    refl,
end

lemma definition.injectivite :
injective f ↔ ∀ {x x' : X}, (f x = f x' → x = x')
:=
/- dEAduction
PrettyName
    Application injective
ImplicitUse
    True
-/
begin
    refl,
end

lemma definition.surjectivite :
surjective f ↔ ∀ y : Y, ∃ x : X, y = f x
:=
/- dEAduction
PrettyName
    Application surjective
ImplicitUse
    True
-/
begin
    refl,
end

lemma theorem.image_singleton :
∀ {f: X→Y}, ∀{x_0: X},
 f '' {x_0} = {f(x_0)}
:=
/- dEAduction
PrettyName
  Image d'un singleton
-/
begin
    todo
end

lemma theorem.image_paire :
∀ {f: X→Y}, ∀{x_0 x_1: X},
 f '' (pair x_0 x_1) = pair (f x_0) (f x_1)
:=
/- dEAduction
PrettyName
  Image d'une paire
-/
begin
  todo
end

end applications

end definitions

-----------------
--- EXERCICES ---
-----------------
namespace exercices

-- variables  {A A': set X}
-- variables {f: X → Y} {g: Y → Z} {B B': set Y}


lemma exercise.exo_23
(f: X → Y)
(H : injective f) :
∀ A B: set X,  f '' (A) ∩ f '' (B) ⊆ f '' (A ∩ B)
:=
/- dEAduction
PrettyName
  Image directe et intersection
-/
begin
  todo
end

lemma exercise.exo_20
(f: X → Y)
(H: injective f) :
∀ A, f ⁻¹' (f '' (A)) ⊆ A
:=
/- dEAduction
PrettyName
  Image réciproque de l'image, et injectivité
-/
begin
  todo
end



end exercices

end ensembles_et_applications

end course
