# Метод Ньютона

## Одномерный метод Ньютона

### ***Теорема Лагранжа о конечных приращениях***

> Пусть функция $f(x)$ дифференцируема в открытом промежутке $(a, b)$ и сохраняет непрерывность на концах этого промежутка.
> Тогда существует такая точка $c \in (a, b)$, что $$f'(c) = \frac{f(b) - f(a)}{b - a}$$

Пусть задана функция $f : X \subseteq  \mathbb{R}  \rightarrow  \mathbb{R}$, имеющая нуль в точке $x^{*}$.<br />
Тогда $\forall x \in X \looparrowright f(x) - f(x^*) = f'(\xi)(x-x^*)$