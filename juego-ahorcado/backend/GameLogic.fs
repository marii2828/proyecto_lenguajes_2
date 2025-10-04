//Manja la logica del juego; las letras que se ingresan, si son parte de la palabara, 
//si son incorrectas, si ya se habían ingresado con anterioridad, etc.

module Hangman.GameLogic

open Hangman.GameState

//verifica si la letra ingresada es parte de la palabra
//si es asi, se agrega a la lista de letras adivinadas
//si no, se agrega a la lista de letras incorrectas
//si la letra ya se había ingresado con anterioridad, se retorna un mensaje de error
//si la letra es incorrecta, se incrementa el contador de intentos incorrectos
//si el contador de intentos incorrectos es igual a la cantidad de intentos maximos, se retorna un mensaje de perdida
//si la letra es correcta, se retorna un mensaje de que se ha ganado el jeugo 
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

//obtiene el estado actual del juego; la palabra oculta, la cantidad de intentos restantes, 
//las letras incorrectas
let getGameInfo gameState =
    let maskedWord = getMaskedWord gameState
    let remaining = getRemainingAttempts gameState
    let incorrectLetters = 
        gameState.GuessedLetters 
        |> List.filter (fun c -> not (gameState.Word.Contains(string c)))
    
    maskedWord, remaining, incorrectLetters