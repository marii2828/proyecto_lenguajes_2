//Maneja el estado del juego; la palabra, las letras adivinadas, los intentos incorrectos, etc.
//se define un type que contiene la palabra, las letras adivinadas, los intentos incorrectos, etc, 
//la cantidad de intentos maximos y si aun se esta jugando

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

//crea el estado inicial del juego 
let initialGameState (word: string) (maxAttempts: int) = {
    Word = word.ToUpper()
    GuessedLetters = []
    IncorrectGuesses = 0
    MaxAttempts = maxAttempts
    Status = Playing
}

//obtiene la palabra oculta; si la letra esta en la lista de letras adivinadas, se muestra, 
//sino, se muestra un guion bajo
let getMaskedWord gameState =
    gameState.Word
    |> Seq.map (fun c -> 
        if List.contains c gameState.GuessedLetters then string c else "_")
    |> String.concat " "

//obtiene la cantidad de intentos restantes
let getRemainingAttempts gameState =
    gameState.MaxAttempts - gameState.IncorrectGuesses

//verifica si el juego ha terminado
let isGameOver gameState =
    match gameState.Status with
    | Playing -> false
    | _ -> true