namespace Sopa.Core

module Solver =
    open Sopa.Core

    let directions =
        [ for dr in -1..1 do
            for dc in -1..1 do
                if not (dr = 0 && dc = 0) then yield (dr, dc) ]

    let vecinos (grid:Grid) (p:Coord) =
        directions
        |> List.map (fun (dr, dc) -> { r = p.r + dr; c = p.c + dc })
        |> List.filter (fun n ->
            n.r >= 0 && n.c >= 0 &&
            n.r < grid.Length &&
            n.c < grid.[0].Length)

    let extender (grid:Grid) (word:string) (path:Coord list) =
        let nextIndex = path.Length
        if nextIndex >= word.Length then
            []
        else
            let nextChar = word.[nextIndex]
            match path with
            | [last] ->
                vecinos grid last
                |> List.filter (fun n -> grid.[n.r].[n.c] = nextChar)
                |> List.map (fun n -> n :: path)
            | last :: second :: _ ->
                let dr = last.r - second.r
                let dc = last.c - second.c
                let next = { r = last.r + dr; c = last.c + dc }
                if next.r >= 0 && next.c >= 0 &&
                    next.r < grid.Length &&
                    next.c < grid.[0].Length &&
                    grid.[next.r].[next.c] = nextChar then
                    [ next :: path ]
                else
                    []
            | _ -> []

    let rec profundidad (expandir:'a -> 'a list) (frontera:'a list) =
        seq {
            match frontera with
            | [] -> ()
            | x::xs ->
                yield x
                yield! profundidad expandir (expandir x @ xs)
        }

    let solve (grid:Grid) (words:string list) =
        words
        |> List.collect (fun w ->
            let iniciales =
                [ for r in 0 .. grid.Length - 1 do
                    for c in 0 .. grid.[0].Length - 1 do
                        if grid.[r].[c] = w.[0] then yield [{ r = r; c = c }] ]

            profundidad (extender grid w) iniciales
            |> Seq.filter (fun path -> path.Length = w.Length)
            |> Seq.map List.rev
            |> Seq.map (fun p -> { word = w; path = p })
            |> Seq.toList)
