open System
open System.Text
open System.Text.Json
open System.Text.Json.Serialization
open FSharp.SystemTextJson
open Sopa.Core
open Sopa.Core.Generator
open Sopa.Core.Validator
open Sopa.Core.Solver

[<EntryPoint>]
let main argv =
    Console.InputEncoding  <- Encoding.UTF8
    Console.OutputEncoding <- Encoding.UTF8

    if argv.Length = 0 then
        eprintfn "Uso: Sopa.Cli <generate|validate|solve>"
        1
    else
        let op = argv.[0].ToLowerInvariant()
        let json = Console.In.ReadToEnd()
        let options = JsonSerializerOptions(WriteIndented = false)
        options.Converters.Add(JsonFSharpConverter())

        let write obj =
            let s = JsonSerializer.Serialize(obj, options)
            Console.Out.Write(s)
            0

        match op with
        | "generate" ->
            let req = JsonSerializer.Deserialize<GenerateRequest>(json, options)
            let size =
                match req.size with
                | Some s -> s
                | None -> req.words |> List.map (fun w -> w.Length) |> List.max
            let seed = defaultArg req.seed 42
            let (grid, placements) = Generator.generate seed size req.words
            write { grid = grid; placements = placements }

        | "validate" ->
            let req = JsonSerializer.Deserialize<ValidateRequest>(json, options)
            let res = Validator.validate req.grid req.wordsRemaining req.selection
            write { found = res.found; word = res.word; path = res.path }

        | "solve" ->
            let req = JsonSerializer.Deserialize<SolveRequest>(json, options)
            let sols = Solver.solve req.grid req.wordsRemaining
            write { solutions = sols }

        | _ ->
            eprintfn "Operación desconocida"
            1