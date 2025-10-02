module Hangman.GameState

type GameStatus = 
    | Playing
    | Won
    | Lost

type GameState = {
    Word: string
    GuessedLetters: char list
    IncorrectGuesses: int
    MaxAttempts: int
    Status: GameStatus
}

let initialGameState (word: string) (maxAttempts: int) = {
    Word = word.ToUpper()
    GuessedLetters = []
    IncorrectGuesses = 0
    MaxAttempts = maxAttempts
    Status = Playing
}

let getMaskedWord gameState =
    gameState.Word
    |> Seq.map (fun c -> 
        if List.contains c gameState.GuessedLetters then string c else "_")
    |> String.concat " "

let getRemainingAttempts gameState =
    gameState.MaxAttempts - gameState.IncorrectGuesses

let isGameOver gameState =
    match gameState.Status with
    | Playing -> false
    | _ -> true