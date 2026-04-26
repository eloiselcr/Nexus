# Spécifications Fonctionnelles (NexusGraph V2)

Ce document est la seule source de vérité pour les règles métier de NexusGraph. Il a été simplifié pour éviter toute "usine à gaz" et garantir une utilisation fluide et prévisible.

## 1. Concept Fondamental : Tout est une Page
Il n'y a plus de distinction entre "Notes" et "Entités". Tout élément dans NexusGraph est une **Page**.
Chaque Page possède :
- Un Titre et un Contenu (texte libre).
- Une **Catégorie** obligatoire (définie à la création).
- Un **Emplacement** (soit un Espace, soit le Global).
- Des Propriétés (clés/valeurs liées à sa catégorie, ex: Email pour une Personne).

---

## 2. L'Emplacement : Flux vs Stock (Silos Stricts)

L'application divise l'information en deux mondes étanches :

### A. Les Espaces (Le "Flux")
- Ce sont les silos opérationnels (ex: le projet LIMEA, le SI AXONE).
- Les pages qui y vivent sont des documents de travail : Comptes-rendus, Points techniques, Suivis.
- **Règle du Silo Strict** : Quand on est dans un Espace, on ne voit *rien* des autres Espaces. 

### B. Le Global (Le "Stock")
- C'est le référentiel transverse de l'entreprise (ex: Personnes, Organisations, Savoirs transverses).
- Techniquement, le Global n'est pas un Espace : ce sont toutes les pages qui ont `Emplacement = Aucun`.
- Ces pages sont accessibles par tous les Espaces via les `@mentions`.

---

## 3. Le Cycle de vie et la Mutation (Simple)

Pour éviter les usines à gaz, la mutation d'une information suit des règles très simples :

- **Changement d'Espace** : Une page peut être déplacée d'un Espace vers le Global (ou vice-versa) en un clic.
- **Changement de Catégorie** : Il n'est pas recommandé de changer la Catégorie d'une page après sa création, car cela effacerait ses propriétés spécifiques. Si une note de réunion contient un savoir important, la bonne pratique est de **créer une nouvelle page Savoir dans le Global**, et de faire un lien vers celle-ci depuis la note de réunion.
- **Corbeille (Soft Delete)** : Lorsqu'une note ou un Espace est supprimé, il n'est pas détruit immédiatement. Il part dans une "Corbeille" (statut supprimé) pendant 30 jours, puis est détruit définitivement. La suppression d'un Espace place automatiquement toutes ses notes dans la corbeille.

---

## 4. Les Liens et la Logique du Graphe (La Lampe Torche)

Les pages sont reliées entre elles uniquement par le mécanisme des **`@mentions`**.
Quand on tape `@Adil` dans une note, un lien direct est créé entre la note et la page d'Adil.

### Règle d'affichage du Graphe (Le Focus)
Pour éviter l'effet "plat de spaghettis", le graphe affiche uniquement le voisinage immédiat selon la règle de la lampe torche :
1. **Focus Local** : Quand on regarde le graphe d'une page dans l'Espace LIMEA, on voit la page et ses liens directs (ex: autres notes LIMEA, ou Personnes du Global mentionnées).
2. **Silo Strict (Fermeture)** : Si la page LIMEA mentionne Adil (qui est dans le Global), le lien s'affiche. Mais si on clique sur Adil dans le graphe, on ne verra **jamais** que Adil est aussi relié à AXONE. Le contexte d'AXONE ne "fuite" pas dans LIMEA.

---

## 5. L'Interface Utilisateur (Les Vues)

1. **Dashboard** : Vue d'ensemble avec les métriques et les dernières pages modifiées.
2. **Sidebar** :
   - Liste des Espaces opérationnels.
   - Liste des Catégories du Global (Personnes, Organisations...) permettant d'accéder au référentiel.
3. **Vue d'un Espace (Kanban)** : Affiche les pages de l'Espace, regroupées en colonnes par Catégories. Permet la création rapide d'une page locale.
4. **Vue Page Universelle** : L'interface de travail divisée en deux panneaux (Éditeur à gauche, Graphe contextuel à droite), redimensionnables via un slider.
