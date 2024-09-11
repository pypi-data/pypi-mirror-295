define([
    'knockout',
    'templates/views/components/plugins/accessibility.htm'
], function(ko,accessibilityPluginTemplate) {

    return ko.components.register('accessibility', {
        template: accessibilityPluginTemplate
    });

});