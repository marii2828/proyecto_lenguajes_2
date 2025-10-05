namespace Sopa.Core

open Sopa.Core

type GenerateRequest  = { words:string list; size:int option; seed:int option }
type GenerateResponse = { grid:Grid; placements:Placement list }

type Selection = { start:Coord; ``end``:Coord }
type ValidateRequest  = { grid:Grid; wordsRemaining:string list; selection:Selection }
type ValidateResponse = { found:bool; word:string option; path:Path option }

type SolveRequest     = { grid:Grid; wordsRemaining:string list }
type SolveResponse    = { solutions:Placement list }