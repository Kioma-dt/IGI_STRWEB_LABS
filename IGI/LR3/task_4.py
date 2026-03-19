"""
Program to Analyze Text (Number of Words; The Longest Word; Every Even Word)
Lab Work 3
Version: 1.0
Developer: Avramenko Roman Aleksandrovich
Date: 19-03-2026
"""

import user_input
from os import system

base_text = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."


def parse_text(text : str) -> list[str]:
    """
    Divide Text into Words 
    
    Args:
        text: Dividable Text

    Returns:
        list: [words]
    """

    words = text.split(' ')
    words = [word.strip(".,") for word in words]

    return words


def count_number_of_words(words : list[str]) -> int:
    """
    Counts Number of Words in Parsed Text
    
    Args:
        words: Parsed Text

    Returns:
        int: Number of Words
    """

    return len(words)


def find_longest_word (words : list[str]) -> tuple[int, str]:
    """
    Finds the Longest Word and It's Position in Parsed Text
    
    Args:
        words: Parsed Text

    Returns:
        tuple: [index, the longest word]
    """

    longest = max(words, key=len)
    position = words.index(longest) + 1

    return (position, longest)


def filter_even_words (words : list[str]) -> list[str]:
    """
    Filter Only Even Words in Parsed Text
    
    Args:
        words: Parsed Text

    Returns:
        list: [even words]
    """

    return words[1::2]


def menu() -> None:
    """
    Menu for Task_4
    """

    while True:
        try:
            system("clear")

            print("Program to Analyze Text (Number of Words; The Longest Word; Every Even Word)")
            print("Lab Work 3")
            print("Version: 1.0")
            print("Developer: Avramenko Roman Aleksandrovich")
            print("Date: 19-03-2026")
            print()

            print("Base Text: ", base_text, '\n', sep="")

            text_parsed = parse_text(base_text)
            words_count = count_number_of_words(text_parsed)
            longest_word_position, longest_word = find_longest_word(text_parsed)
            words_even = filter_even_words(text_parsed)
            
            # Output
            print(f"Number of Words: {words_count}\n")    
            print(f"Longest Word: \"{longest_word}\" on Position: {longest_word_position}\n") 
            print("Even words: ", end = "")
            print(*words_even, sep=", ")    

        except ValueError as e:
            print(f"Value Error: {e}")

        except Exception as e:
            print(f"Error: {e}")

        finally:
            if not user_input.get_yes_or_no("\nWould You Like to Try Again? (yes / no)"):
                break


# If module is executing run it
if __name__ == "__main__":
    menu()
