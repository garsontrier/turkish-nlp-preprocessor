# Written by Güray Baydur
# DEPRECATED
def get_last_two_vowels(word):
    turkish_vowels = ['e', 'i', 'ö', 'ü', 'a', 'ı', 'o', 'u']
    vowel_list = []
    count = 2
    if word:
        for i in range(len(word) - 1, -1, -1):
            if word[i] in turkish_vowels and count != 0:
                vowel_list.append(word[i])
                count -= 1
    vowel_list.reverse()
    return vowel_list


def is_vovel_harmonic_for_frontness(word):
    front_produced_vowels = ['e', 'i', 'ö', 'ü']
    back_produced_vowels = ['a', 'ı', 'o', 'u']
    last_vowels = get_last_two_vowels(word)
    if len(last_vowels) == 1:
        return True
    else:
        return all(elem in front_produced_vowels for elem in last_vowels) or all(
            elem in back_produced_vowels for elem in last_vowels)


def is_vovel_harmonic_for_roundness(word):
    rounded_vowels = ['o', 'ö', 'u', 'ü']
    unrounded_vowels = ['a', 'e', 'ı', 'i']
    last_vowels = get_last_two_vowels(word)
    if len(last_vowels) == 1:
        return True
    else:
        unrounded_check = all(elem in unrounded_vowels for elem in last_vowels)
        other_rule = last_vowels[0] in rounded_vowels and last_vowels[1] in ['a', 'e', 'u', 'ü']

        return unrounded_check or other_rule

def get_vowel_harmony(word):
    vowel_harmony_system = {"Frontness": is_vovel_harmonic_for_frontness(word),"Roundness": is_vovel_harmonic_for_roundness(word)}
    return vowel_harmony_system


if __name__ == '__main__':
    word = "onunla"
    print(word)
    print(get_last_two_vowels(word))
    print("is_vovel_harmonic_for_frontness: " + str(is_vovel_harmonic_for_frontness(word)))
    print("is_vovel_harmonic_for_roundness: " + str(is_vovel_harmonic_for_roundness(word)))
    print(get_vowel_harmony(word))