namespace Sopa.Core

module Validator =
    open Sopa.Core
    open System

    type ValidationResult = { found:bool; word:string option; path:Path option }

    let validate (grid:Grid) (wordsRemaining:string list) (sel:Selection) : ValidationResult =
        let dr = Math.Sign(sel.``end``.r - sel.start.r)
        let dc = Math.Sign(sel.``end``.c - sel.start.c)
        let mutable path = []
        let mutable r, c = sel.start.r, sel.start.c
        let mutable word = ""
        while r <> sel.``end``.r + dr || c <> sel.``end``.c + dc do
            path <- {r=r; c=c} :: path
            word <- word + string grid.[r].[c]
            r <- r + dr
            c <- c + dc
        path <- List.rev path
        let found = wordsRemaining |> List.exists (fun w -> w = word || w = new string(word.ToCharArray() |> Array.rev))
        { 
            found = found
            word = if found then Some word else None
            path = if found then Some path else None 
        }