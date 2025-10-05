namespace Sopa.Core
open System

module Generator =

    type Dir = { dr:int; dc:int }

    let directions =
        [ for dr in -1..1 do
            for dc in -1..1 do
                if not (dr=0 && dc=0) then yield {dr=dr; dc=dc} ]

    let private cabe (size:int) (r:int) (c:int) (dir:Dir) (word:string) =
        let endR = r + dir.dr * (word.Length - 1)
        let endC = c + dir.dc * (word.Length - 1)
        endR >= 0 && endR < size && endC >= 0 && endC < size

    let private intentarColocar (grid:char[][]) (r:int) (c:int) (dir:Dir) (word:string) =
        let size = grid.Length
        if not (cabe size r c dir word) then false else
        let mutable ok = true
        for i in 0..word.Length-1 do
            let rr, cc = r + dir.dr*i, c + dir.dc*i
            let existing = grid.[rr].[cc]
            if existing <> '\000' && existing <> word.[i] then ok <- false
        if ok then
            for i in 0..word.Length-1 do
                let rr, cc = r + dir.dr*i, c + dir.dc*i
                grid.[rr].[cc] <- word.[i]
            true
        else false

    let generate (seed:int) (size:int) (words:string list) : Grid * Placement list =
        let rnd = Random(seed)
        let grid = Array.init size (fun _ -> Array.create size '\000')
        let placements = ResizeArray<_>()

        for w in words do
            let mutable placed = false
            let mutable tries = 0
            while not placed && tries < 1000 do
                tries <- tries + 1
                let r, c = rnd.Next(size), rnd.Next(size)
                let dir = directions.[rnd.Next(directions.Length)]
                if intentarColocar grid r c dir w then
                    placed <- true
                    let path = [ for i in 0..w.Length-1 -> {r=r + dir.dr*i; c=c + dir.dc*i} ]
                    placements.Add({word=w; path=path})

        let alphabet = [|'A'..'Z'|]
        for r in 0..size-1 do
            for c in 0..size-1 do
                if grid.[r].[c] = '\000' then
                    grid.[r].[c] <- alphabet.[rnd.Next alphabet.Length]

        let gridStr = grid |> Array.map (fun row -> String(row))
        let placementsList = placements |> Seq.toList
        gridStr, placementsList
