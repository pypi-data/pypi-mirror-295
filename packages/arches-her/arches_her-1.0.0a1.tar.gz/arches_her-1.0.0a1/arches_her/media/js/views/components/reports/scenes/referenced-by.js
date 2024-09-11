define([
    'jquery',
    'underscore',
    'knockout',
    'arches',
    'utils/report',
    'templates/views/components/reports/scenes/referenced-by.htm',
    'bindings/datatable',
    'bindings/reports'], 
function($, _, ko, arches, reportUtils, ReferencedByTemplate) {
    return ko.components.register('views/components/reports/scenes/referenced-by', {
        viewModel: function(params) {
            const self = this;
            Object.assign(self, reportUtils);
            self.resourceinstanceid = params.resourceInstanceId;
            self.graphsArray = params.graphs;
            self.graphsList = [];
            self.graphs = [];
            self.relations = ko.observableArray();
            self.visible = {
                referencedBy: ko.observable(true),
            };

            // referenced by table configuration
            self.referencedByTwoColumnTableConfig = {
                ...self.defaultTableConfig,
                "paging": true,
                "searching": true,
                "columns": Array(2).fill(null),
                "bDestroy": true
            };

            self.getGraphs = function(){
                return $.ajax({
                    url: arches.urls.graphs_api,
                    context: this,
                }).done(function(graphsResponse) {
                    self.graphs = ko.unwrap(graphsResponse);
                    self.graphsList = [];
                    for(let g in self.graphsArray){
                        var graphFindResult = self.graphs.find((gr) => gr.name === self.graphsArray[g]);
                        self.graphsList.push(graphFindResult.graphid);
                    }
                    return;
                }).fail(function() {
                    // error
                });
            };


            self.getRelatedResources = function(){
                return $.ajax({
                    url: arches.urls.related_resources + self.resourceinstanceid,
                    context: self,
                })
                    .done(function(response) {
                        self.getGraphs().then(function(){
                            var responseRelatedResources = response.related_resources.related_resources;
                            self.relations.removeAll();
                            for(let r in responseRelatedResources){
                                var responseRelatedResource = responseRelatedResources[r];
                                if(self.graphsList.includes(responseRelatedResource["graph_id"] )){
                                    var graphName = (self.graphs.find((gr) => gr.graphid === responseRelatedResource["graph_id"]))["name"];
                                    self.relations.push({"related_resource_name": responseRelatedResource["displayname"], "related_resource_link": arches.urls.resource_report + responseRelatedResource["resourceinstanceid"], "related_resource_type": graphName});
                                }
                            }
                            return;
                        });
                    })
                    .fail(function() {
                        // error
                    });
            };

            self.getRelatedResources();
        },
        template: ReferencedByTemplate
    });
});