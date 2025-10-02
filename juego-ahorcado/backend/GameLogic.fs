module Hangman.GameLogic

open Hangman.GameState

let makeGuess guess gameState =
    let guessUpper = System.Char.ToUpper(guess)
    
    if List.contains guessUpper gameState.GuessedLetters then
        gameState, "Ya intentaste esta letra"
    else
        let newGuessedLetters = guessUpper :: gameState.GuessedLetters
        let isInWord = gameState.Word.Contains(string guessUpper)
        
        let newIncorrectGuesses = 
            if isInWord then gameState.IncorrectGuesses 
            else gameState.IncorrectGuesses + 1
        
        let won = 
            not (System.String.IsNullOrEmpty(gameState.Word)) &&
            gameState.Word 
            |> Seq.forall (fun c -> List.contains c newGuessedLetters)
        
        let lost = newIncorrectGuesses >= gameState.MaxAttempts
        
        let newStatus =
            if won then Won
            elif lost then Lost
            else Playing
        
        let newGameState = {
            gameState with
                GuessedLetters = newGuessedLetters
                IncorrectGuesses = newIncorrectGuesses
                Status = newStatus
        }
        
        let message =
            if won then "¡Ganaste! La palabra era: " + gameState.Word
            elif lost then "¡Perdiste! La palabra era: " + gameState.Word
            elif isInWord then "¡Buen trabajo! La letra esta en la palabra"
            else "Letra incorrecta"
        
        newGameState, message

let getGameInfo gameState =
    let maskedWord = getMaskedWord gameState
    let remaining = getRemainingAttempts gameState
    let incorrectLetters = 
        gameState.GuessedLetters 
        |> List.filter (fun c -> not (gameState.Word.Contains(string c)))
    
    maskedWord, remaining, incorrectLetters