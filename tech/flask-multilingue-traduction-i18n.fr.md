<!-- 
.. title: Site multilingue avec python, Flask et Babel
.. slug: flask-multilingue-traduction-i18n-babel-python
.. date: 2016-03-05 22:49:20 UTC+02:00
.. tags: flask, python, babel, i18n, private
.. category: 
.. link: 
.. description: 
.. type: text
-->

S'il y a un truc qui m'énerve, c'est de devoir faire 20 blogs/posts stackoverflow pour trouver ce qu'il me faut pour faire un truc aussi simple que d'écrire un site multilingue. Alors voilà, j'ai tout compilé ici.<!-- TEASER_END -->

Je suis relativement novice en python/Flask et tout le toutim, donc certaines choses vont peut-être choquer les puristes. Mais j'ai dans l'idée que ça pourrait en aider d'autres. Ce post est tiré du code que j'ai réalisé pour écrire le site de mon livre <a href="http://vimebook.com">Vimebook</a> en français/anglais.

Mes pré-requis étaient :

- Traduction des menus/label dans la langue
- Affichage de contenu différent en fonction de la langue
- Passage d'une langue à l'autre par click sur un lien

