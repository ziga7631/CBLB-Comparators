## 1-bit magnitude comparator implementation using biological logic blocks

### Building the model

Osnovna implementacija 1-bitnega primerjalnika v digitalnih vezjih:

![1-bit comparator digital circuit](slike/1_bit_magnitude_comparator/png/1_bit_comparator_original_white.drawio.png)

Biološki gradniki podpirajo le vrata OR in NOT, zato potrebujemo vezje pretvoriti tako, da bo uporabljalo le te gradnike.

Predelano vezje:
![1-bit comparator converted to only use not and or gates](slike/1_bit_magnitude_comparator/png/1_bit_comparator_or_not_with_model_notation_without_notation_white.drawio.png)

V modelu **comparator_model** (_1\_bit\_comparator.ipynb_) shranjujemo rezultate po naslednji shemi:
![1-bit comparator converted to only use not and or gates with notation](slike/1_bit_magnitude_comparator/png/1_bit_comparator_or_not_with_model_notation_with_notation_white.drawio.png)

### Testing the model

![A0B0](slike/1_bit_magnitude_comparator/png/comparator_A0_B0.png)
![A0B1](slike/1_bit_magnitude_comparator/png/comparator_A0_B1.png)
![A1B0](slike/1_bit_magnitude_comparator/png/comparator_A1_B0.png)
![A1B1](slike/1_bit_magnitude_comparator/png/comparator_A1_B1.png)