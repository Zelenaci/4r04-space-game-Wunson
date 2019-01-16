# PRG-SpaceGame

Jedná se zatím pouze o prototyp vesmírné střílečky pro 2 hráče. Hráči mohou hrát dle domluvy buď proti sobě, nebo společně proti nepřátelským raketám. Část raket je naváděna na hráče 1, část zase na hráče 2. Všechny rakety lze sestřelit.
Po zásahu raketou se hráč objeví na novém náhodném místě a může hrát znovu. Do budoucna by to chtělo přidat ještě nějaké počítadlo skóre.

## Ovládání:

### Hráč 1:
* <b>Pohyb:</b> UP, DOWN, LEFT, RIGHT
* <b>Střelba:</b> M

### Hráč 2:
* <b>Pohyb:</b> W, S, A, D
* <b>Střelba:</b> Q

Ovládání lodí by se mělo chovat podobně, jako ve skutečném mezihvězdném prostoru. Každá loď, ale i všechny ostatní objekty, má tedy určitý vektor pohybu. Při zážehu trysky se pak mění velikost, případně směr tohoto vektoru. Maximální velikost vektoru, tedy maximální rychlost je u každého objektu omezena. Pro lepší ovladatelnost všechny objekty také neustále brzdí. Pokud tedy vypneme trysky, naše loď po chvilce sama zastaví. Zmáčknutím klávesy pro směr lze pak brždění ještě urychlit.