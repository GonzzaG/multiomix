from django.urls import path
from . import views


urlpatterns = [
    path('gene-information', views.GeneInformation.as_view(), name='gene_information'),
    path('pathways-information', views.PathwaysInformation.as_view(), name='pathways_information'),
    path(
        'metabolic-pathways-information',
        views.MetabolicPathwaysInformation.as_view(),
        name='metabolic_pathways_information'
    ),
    path('gene-ontology-gene-terms', views.GeneOntologyTermsOfGene.as_view(), name='gene_ontology_gene_terms'),
    path('gene-ontology-term-terms', views.GeneOntologyTermsOfTerm.as_view(), name='gene_ontology_term_terms')
]
