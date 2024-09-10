/-
This is a d∃∀duction file providing first exercises about quantifiers and numbers.
French version.
-/

-- Lean standard import
import data.real.basic
import tactic

-- dEAduction tactics
-- structures2 and utils are vital
import deaduction_all_tactics
-- import structures2      -- hypo_analysis, targets_analysis
-- import utils            -- no_meta_vars
-- import compute_all      -- Tactics for the compute buttons
-- import push_neg_once    -- Pushing negation just one step
-- import induction        -- Induction theorems

-- dEAduction definitions
-- import set_definitions
-- import real_definitions

-- Use classical logic
local attribute [instance] classical.prop_decidable


-- General principles :
-- Type should be defined as parameters, in order to be implicit everywhere
-- other parameters are implicit in definitions, i.e. defined using '{}' (e.g. {A : set X} )
-- but explicit everywhere else, i.e. defined using '()' (e.g. (A : set X) )
-- each definition must be an iff statement (since it will be called with 'rw' or 'symp_rw')



---------------------
-- Course metadata --
---------------------
/- dEAduction
Title
    Logique et inégalités
Description
    Deux exercices "Vrai ou Faux" sur les nombres réels.
OpenQuestion
    True
AvailableExercises
    NONE
AvailableLogic
    ALL -not
Display
    VraiFaux --> ("Vrai ou faux : ", -1, " ?")
-/

-- If OpenQuestion is True, DEAduction will ask the user if she wants to
-- prove the statement or its negation, and set the variable
-- NegateStatement accordingly
-- If NegateStatement is True, then the statement will be replaced by its
-- negation
-- AvailableExercises is set to None so that no exercise statement can be applied
-- by the user. Recommended with OpenQuestions set to True!


local attribute [instance] classical.prop_decidable

---------------------------------------------
-- global parameters = implicit variables --
---------------------------------------------
section course

namespace Logique_et_nombres_reels
/- dEAduction
PrettyName
    Logique et nombres réels
-/

namespace negation
/- dEAduction
PrettyName
    Enoncés de négation
-/

lemma theorem.negation_et {P Q : Prop} :
( not (P and Q) ) ↔ ( (not P) or (not Q) )
:=
/- dEAduction
PrettyName
    Négation du 'et'
-/
begin
    exact not_and_distrib
end

lemma theorem.negation_ou {P Q : Prop} :
( not (P or Q) ) ↔ ( (not P) and (not Q) )
:=
/- dEAduction
PrettyName
    Négation du 'ou'
-/
begin
    exact not_or_distrib
end

lemma theorem.negation_non {P : Prop} :
( not not P ) ↔  P
:=
/- dEAduction
PrettyName
    Négation du 'non'
-/
begin
    exact not_not
end


lemma theorem.negation_implique {P Q : Prop} :
( not (P → Q) ) ↔  ( P and (not Q) )
:=
/- dEAduction
PrettyName
    Négation d'une implication
-/
begin
    exact not_imp,
end


lemma theorem.negation_existe  {X : Type} {P : X → Prop} :
( ( not ∃ (x:X), P x  ) ↔ ∀ x:X, not P x )
:=
/- dEAduction
PrettyName
    Négation de '∃X, P(x)'
-/
begin
    exact not_exists,
end



lemma theorem.negation_pour_tout {X : Type} {P : X → Prop} :
( not (∀x, P x ) ) ↔ ∃x, not P x
:=
/- dEAduction
PrettyName
    Négation de '∀x, P(x)'
-/
begin
    exact not_forall
end


lemma theorem.negation_inegalite_stricte {X : Type} (x y : X) [linear_order X]:
( not (x < y) ) ↔ y ≤ x
:=
/- dEAduction
PrettyName
    Négation de 'x < y'
-/
begin
    exact not_lt
end


lemma theorem.negation_inegalite_large {X : Type} (x y : X) [linear_order X]:
( not (x ≤ y) ) ↔ y < x
:=
/- dEAduction
PrettyName
    Négation de 'x ≤ y'
-/
begin
    exact not_le
end

lemma theorem.double_negation (P: Prop) :
(not not P) ↔ P :=
/- dEAduction
PrettyName
    Double négation
-/
begin
    todo
end


end negation

def VraiFaux (P:Prop) : Prop := P ∨ ¬ P


namespace exercices
/- dEAduction
PrettyName
    Exercices
-/

lemma exercise.vraifaux1 :
(∀x:ℝ, x ≤ x^2)
:=
/- dEAduction
PrettyName
    Vrai ou Faux ? Pour tout x dans ℝ, x ≤ x^2
-/
begin
    todo
end

lemma exercise.vraifaux2 :
(∀x:ℝ, ∃y:ℝ, x+y >0)
:=
/- dEAduction
PrettyName
    Vrai ou Faux ? Pour tout x dans ℝ, il existe un y dans ℝ tel que x + y > 0
-/
begin
    todo
end

end exercices

end Logique_et_nombres_reels

end course