//Extrae la palabra del archivo words.txt

module Hangman.WordManager

open System
open System.IO

let randomGenerator = Random()

let getWord (rutaArchivo: string) : string option =
    let palabras =
        try
            File.ReadAllLines(rutaArchivo)
            |> Array.toList
        with
        | _ -> []

    match palabras with
    | [] -> None
    | lista ->
        let indice = randomGenerator.Next(List.length lista)
        Some (List.item indice lista)

let getRandomWord () =
    match getWord "words.txt" with
    | Some palabra -> palabra.ToUpper()
    | None -> "PROGRAMACION" 