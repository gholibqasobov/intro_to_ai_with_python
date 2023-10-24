import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])
    # people = load_data("C:\Python3\Introduction to AI with Python\Lecture 2\Project 2\heredity\data/family0.csv")
    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    """
    people = {
        james: {
            name: james,
            mother: lily,
            father: mark,
            trait: None
            }
        }
        
    probabilities = {
        james: {
            gene: {}
            }, 
        trait: {}
    }
    """

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]



def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    p = 1
    for person in people:
        # check for parents
        if people[person]['mother'] is None and people[person]['father'] is None:
            # check number of genes
            if person in one_gene:
                gene_num = 1
            elif person in two_genes:
                gene_num = 2
            else:
                gene_num = 0

            # check for trait
            if person in have_trait:
                has_trait = True
            else:
                has_trait = False

            # define the probability
            prob = PROBS["gene"][gene_num] * PROBS["trait"][gene_num][has_trait]
        else:
            # conditional probability according to parents

            # check for number of parents' genes
            if people[person]['mother'] in one_gene:
                mother_gene_prob = (1 - PROBS["mutation"]) * 0.5
            elif people[person]['mother'] in two_genes:
                mother_gene_prob = 1 - PROBS["mutation"]
            else:
                mother_gene_prob = PROBS["mutation"]

            if people[person]['father'] in one_gene:
                father_gene_prob = (1 - PROBS["mutation"]) * 0.5
            elif people[person]['father'] in two_genes:
                father_gene_prob = 1 - PROBS["mutation"]
            else:
                father_gene_prob = PROBS["mutation"]

            # check for person's trait
            if person in have_trait:
                has_trait = True
            else:
                has_trait = False
            if person in one_gene:
                # gene either from father or mother, but not both
                prob = (father_gene_prob * (1 - mother_gene_prob) + mother_gene_prob * (1 - father_gene_prob)) * PROBS["trait"][1][has_trait]
            elif person in two_genes:
                # genes from both parents
                prob = (father_gene_prob * mother_gene_prob) * PROBS["trait"][2][has_trait]
            else:
                # genes from none of parents (with probability of mutation)
                prob = ((1 - father_gene_prob) * (1 - mother_gene_prob)) * PROBS["trait"][0][has_trait]

        p *= prob

    return p


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    """
    Adds new joint distributions to existing distributions in probabilities
    
    accepts five values:
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    
    one_gene = {people with one gene}
    two_genes = {people with two genes}
    have_trait = {people with trait} in the current joint distribution
    
    
    p = probability of joint distribution
    
    
    
    for each person in probabilities, 
    
    
        should update
            probabilities[person]["gene"]
            probabilities[person]["trait"]
            
            by adding p to the appropriate value in each distribution
            
            all other values shold be left unchanged
            
            
            
            
    ex, if "Harry" in two_genes and "Harry" in trait:
            probabilities["harry"]["gene"][2] += p
            probabilities["harry"]["trait"][True]
            
            
    should not return any value

    
    summary: we are given probabilities, one_gene, two_gene, and trait
    
    if person in people in one of those, add p
        
    """
    # raise NotImplementedError

    for person in probabilities:
        if person in one_gene:
            probabilities[person]["gene"][1] += p
        elif person in two_genes:
            probabilities[person]["gene"][2] += p
        else:
            probabilities[person]["gene"][0] += p
        if person in have_trait:
            probabilities[person]["trait"][True] += p
        else:
            probabilities[person]["trait"][False] += p



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    # raise NotImplementedError
    """
    the approach is going to be this way:
    sum all the values in each distribution and divide each value by that distribution
    
    let's check
    """

    for person in probabilities:
        gene_sum = sum(probabilities[person]['gene'].values())
        trait_sum = sum(probabilities[person]['trait'].values())

        probabilities[person]['gene'] = {genes: (prob/gene_sum) for genes, prob in probabilities[person]['gene'].items()}
        probabilities[person]['trait'] = {trait: (prob/gene_sum) for trait, prob in probabilities[person]['trait'].items()}



if __name__ == "__main__":
    main()
