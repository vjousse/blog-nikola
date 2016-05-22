<!-- 
.. title: Elm lang, le prochain react/redux/angularjs ?
.. slug: elm-lang-prochain-react-redux-angular
.. date: 2016-05-18 20:39:20 UTC+02:00
.. tags: functional programming, javascript, elm
.. category: 
.. link: 
.. description: 
.. type: text
-->

Dans le monde du développement frontend, il y a une nouvelle techno tous les jours. Et encore ça, c'est dans les mauvais jours. Quand j'ai voulu m'y remettre, j'étais forcément un peu perdu. J'avais fais du AngularJS et je ne voulais plus en entendre parler. Dans le coup j'ai demandé sur [Twitter](https://twitter.com/vjousse/status/716893840163082240). [n1k0](https://twitter.com/n1k0) et [MoOx](https://twitter.com/MoOx) m'ont alors montré la voix.<!-- TEASER_END -->

## React/redux : les bons concepts, la grande communauté et javascript

Un consensus semblait se former autour de React+Redux avec webpack pour la boîte à outils et [Immutable.js]() pour les structures de données immuables. Cool, j'avais mon point de départ. J'ai alors suivi deux tutos : [Getting Started with React, Redux and Immutable: a Test-Driven Tutorial](http://www.theodo.fr/blog/2016/03/getting-started-with-react-redux-and-immutable-a-test-driven-tutorial-part-1/) et [Full-Stack Redux Tutorial](http://teropa.info/blog/2015/09/10/full-stack-redux-tutorial.html) dont le premier s'inspirait.

Ce qui m'a principalement séduit dans tout ça, c'est la nouvelle architecture que la communauté autour de ces outils/frameworks promeut. C'est à dire :

1. Les composants de l'interface ne font qu'afficher. Aucun état (ou quasi pas) interne au composant. Les composants sont déclaratifs.
2. L'état de l'application est représenté dans un arbre (state tree). Pour passer d'un état à un autre, on applique une fonction sur cet arbre qui nous donne un nouvel arbre (on ne mute pas l'ancien).
3. Les composants ne font que refléter l'état immuable de l'arbre à l'instant T.
4. Les fonctions sans état (pures) et les données immuables sont encouragées (on commence enfin à se rendre compte que raisonner sur des objets qui ont des états internes est très compliqué).

Pourquoi c'est sexy ça ? Parce qu'enfin on peut :

1. Tester les composants d'affichage simplement. On leur donne juste le sous-ensemble de l'arbre qui les concerne et on voit comment ils se comportent.
2. Facilement débugger le code qui gère le rendu. On connait l'état de l'arbre à chaque interaction, et les composants ne font que refléter cet état. Isoler les soucis est alors plus facile. Pas d'état caché à l'intérieur d'un composant.
3. Tester nos fonctions simplement. Beaucoup moins de choses à mocker/simuler, l'approche fonctionnelle de tout ça permet de n'agir que sur les entrées des fonctions pour tester leur résultat.
4. Facilement réutiliser des composants : ils ne dépendent d'aucune business logic, juste des données passées en paramètre.

Comme diraient mes chers coworkers : trop de swag ! Mais quelque chose continuait de me chiffoner : javascript.

Loin de moi l'idée de faire du "javascript bashing", c'est le langage du frontend web, et rien que pour ça, il est à respecter. Mais j'ai personnellement jamais accroché : trop bordélique, écosystème énorme (trop ?) mais de qualité très variable, difficilement lisible, …
Zut, j'avais trouvé une architecture qui me plaisait (React/Redux/Immutable.js) mais j'avais l'impression que c'était des choses qui auraient du être possibles au niveau du langage lui-même. J'avais la désagréable impression qu'on était en train de patcher Javascript lui-même.

## Elm : les bons concepts, la petite communauté et le bon langage

C'est alors que je me suis rappelé ce dont mes chers amis Twitteriens m'avaient parlé auparavant : [Elm](). Elm c'est React/Redux/Immutable.js mais avec un langage pensé pour.

Elm est un langage de programmation fonctionnel (fonctions pures sans état) statiquement typé (un compilateur qui vous dit avant où sont vos erreurs) pensé pour le frontend et les interfaces graphiques (HTML/CSS, SVG, …). Vous pouvez programmer votre interface entrièrement en Elm, ou alors la connecter avec du Javascript plus classique via un système de ports (qu'on peut voir comme du « Javascript as a service » lorsqu'on fait du Elm).

Elm a plein d'avantages :

1. Par défaut, il force l'architecture vue plus haut avec React/Redux/Immutable.js.
2. Il dispose d'un compilateur convivial (oui c'est possible) qui affiche des conseils en plus des erreurs.
3. Quand ça compile, ça marche. Plus de "undefined is not a function" au runtime.
4. Le système de type et le compilateur permettent de refactorer sereinement. Besoin de moins de tests, et confiance dans le compilateur pour nous dire où on a fait une bêtise.
5. Il est n00b friendly. C'est une des volontés du développeur principal : rendre [la programmation fonctionnelle « Mainstream »](TODO). Et ça, c'est un gros plus.
6. Il s'interface avec Javascript sans sacrifier ce qui fait de lui un bon langage (immuabilité, fonctions sans état, …)

Il a aussi des défauts :

1. L'écosystème est encore petit. Il faut souvent s'interfacer avec du javascript alors qu'on aimerait bien tout faire en Elm.
2. Il est purement fonctionnel, il peut donc dérouter ceux qui viennent d'un langage plus impératif (comme javascript).
3. Il est encore jeune, l'API a donc tendance à changer (le passage d'Elm 0.16 à 0.17 en est un bon exemple).

## Mon avis

J'ai beaucoup été attiré par les langages fonctionnels ces dernières années, mais je n'ai encore jamais réussi à en utiliser un pour de vrai dans mes développements quotidiens. Il y avait souvent trop de contraintes : système de type trop contraignant, équipe réfractaire à la programmation fonctionnelle, langages et communautés d'« élites » pour des « élites ».

Avec Elm, c'est différent. J'ai l'impression que la communauté a compris ces soucis et que son but, c'est d'en faire un langage accessible et utile. Tirer partie des meilleures parties des langages fonctionnels sans amener tout ce dont on se passerait bien.

Avec le changement de mentalité qui se fait dans le monde javascript vers un peu plus de fonctionnel (immuabilité, React/Redux, ES6, …) et Elm qui fait tout pour être attirant, j'ai envie de croire qu'Elm peut être « the next big thing » … enfin, jusqu'à la prochaine :-)
