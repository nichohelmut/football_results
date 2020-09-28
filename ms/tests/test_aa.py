from ms.aa import AA
import numpy as np
from ms.clustering.clustering import ArchetypalAnalysis

archetype = AA()
archetype_model = ArchetypalAnalysis(n_archetypes=5, iterations=3, tmax=300)


def test_european_leagues():
    df = archetype.european_leagues()

    '''['Germany', 'France', 'Spain', 'England', 'Italy'] should be included in df'''
    l_countrie = ['Germany', 'France', 'Spain', 'England', 'Italy']
    assert True == set(l_countrie).issubset(df['country'].unique())

    '''length of df should 98'''
    assert len(df) == 98

    '''number of columns of df should 280'''
    assert len(df.columns) == 280


def test_climbers():
    df = archetype.climbers()

    '''length of df should 7'''
    assert len(df) == 9

    '''number of columns of df should 280'''
    assert len(df.columns) == 280


def test_matrix():
    """number of columns of df should 280"""
    assert type(archetype.matrix()) is np.ndarray


def test_archetypal_transform():
    model = archetype_model.fit(archetype.matrix())
    A = model.transform(archetype.matrix())

    '''A shpuld be an np.darray'''
    assert type(A) is np.ndarray

    '''length of A should be number of archetypes selected in model fitting'''
    assert len(A) == archetype_model.n_archetypes

# TODO: CREATE TEST FOR CHECKING ENUMERATION OF LABELS DICT
# def test_enumaration_of_labels
