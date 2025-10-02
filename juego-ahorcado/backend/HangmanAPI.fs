module Hangman.API

open Hangman.GameState
open Hangman.GameLogic
open Hangman.WordManager
open System.Collections.Generic
open System.IO

type HangmanGame() =
    let mutable currentState = initialGameState "" 6
    
    member this.StartNewGame(?word: string, ?maxAttempts: int) =
        let gameWord = defaultArg word (getRandomWord())
        let attempts = defaultArg maxAttempts 6
        currentState <- initialGameState gameWord attempts
        let masked, remaining, _ = getGameInfo currentState
        (masked, remaining, "¡Juego iniciado!")
    
    member this.MakeGuess guess =
        if String.length guess <> 1 then
            (getMaskedWord currentState, getRemainingAttempts currentState, "Ingresa solo una letra")
        else
            let newState, message = makeGuess (guess.[0]) currentState
            currentState <- newState
            let masked, remaining, incorrect = getGameInfo currentState
            (masked, remaining, message)
    
    member this.GetGameState() =
        let masked, remaining, incorrect = getGameInfo currentState
        let status = 
            match currentState.Status with
            | Playing -> "playing"
            | Won -> "won"
            | Lost -> "lost"
        
        (masked, remaining, incorrect, status, currentState.Word)
    
    member this.GetCurrentWord() =
        currentState.Word
    
    member this.LoadState(state: GameState) =
        currentState <- state
    
    member this.GetRawState() =
        currentState
    
    member this.IsGameOver() =
        isGameOver currentState

let getStateFilePath gameId = sprintf "game_%s.state" gameId

let saveGameState gameId (gameState: GameState) =
    let filePath = getStateFilePath gameId
    let content = sprintf "%s|%s|%d|%d|%s" 
                    gameState.Word 
                    (String.concat "," (List.map string gameState.GuessedLetters))
                    gameState.IncorrectGuesses
                    gameState.MaxAttempts
                    (match gameState.Status with | Playing -> "playing" | Won -> "won" | Lost -> "lost")
    File.WriteAllText(filePath, content)

let loadGameState gameId =
    let filePath = getStateFilePath gameId
    if File.Exists(filePath) then
        try
            let content = File.ReadAllText(filePath)
            let parts = content.Split('|')
            if parts.Length >= 5 then
                let word = parts.[0]
                let guessedLetters = 
                    if System.String.IsNullOrEmpty(parts.[1]) then []
                    else parts.[1].Split(',') |> Array.map (fun s -> s.[0]) |> Array.toList
                let incorrectGuesses = int parts.[2]
                let maxAttempts = int parts.[3]
                let status = match parts.[4] with
                             | "won" -> Won
                             | "lost" -> Lost
                             | _ -> Playing
                Some {
                    Word = word
                    GuessedLetters = guessedLetters
                    IncorrectGuesses = incorrectGuesses
                    MaxAttempts = maxAttempts
                    Status = status
                }
            else None
        with
        | _ -> None
    else None

let deleteGameState gameId =
    let filePath = getStateFilePath gameId
    if File.Exists(filePath) then
        File.Delete(filePath)

let executeCommand args =
    match args with
    | [| "start" |] ->
        let gameId = "default"
        deleteGameState gameId
        let game = HangmanGame()
        let masked, remaining, message = game.StartNewGame()
        saveGameState gameId (game.GetRawState())
        sprintf "%s|%d|%s" masked remaining message
    | [| "start"; gameId |] ->
        deleteGameState gameId
        let game = HangmanGame()
        let masked, remaining, message = game.StartNewGame()
        saveGameState gameId (game.GetRawState())
        sprintf "%s|%d|%s" masked remaining message
    | [| "start"; gameId; word |] ->
        deleteGameState gameId
        let game = HangmanGame()
        let masked, remaining, message = game.StartNewGame(word = word)
        saveGameState gameId (game.GetRawState())
        sprintf "%s|%d|%s" masked remaining message
    | [| "guess"; gameId; letter |] ->
        match loadGameState gameId with
        | Some state ->
            let game = HangmanGame()
            game.LoadState(state)
            let masked, remaining, message = game.MakeGuess(letter)
            saveGameState gameId (game.GetRawState())
            sprintf "%s|%d|%s" masked remaining message
        | None -> "ERROR|0|No hay juego activo. Usa 'start' primero"
    | [| "getword"; gameId |] ->
        match loadGameState gameId with
        | Some state -> sprintf "%s|0|palabra actual" state.Word
        | None -> "ERROR|0|No hay juego activo"
    | [| "status"; gameId |] ->
        match loadGameState gameId with
        | Some state ->
            let masked = getMaskedWord state
            let remaining = getRemainingAttempts state
            let incorrect = state.GuessedLetters |> List.filter (fun c -> not (state.Word.Contains(string c)))
            let status = match state.Status with | Playing -> "playing" | Won -> "won" | Lost -> "lost"
            sprintf "%s|%d|%s|%s|%s" masked remaining (String.concat "," (List.map string incorrect)) status state.Word
        | None -> "ERROR|0|No hay juego activo"
    | _ -> "ERROR|0|Comando no válido"