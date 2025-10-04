//Punto de entrada del programa
//ejecuta el comando que se le pasa como argumento

module Main

open System
open Hangman.API

[<EntryPoint>]
let main argv =
    if argv.Length > 0 then
        let result = executeCommand argv
        printfn "%s" result
    0