(function () {
    'use strict';
    angular.module("isyplus")
        .controller("JobCntrl", JobCntrl);

    function JobCntrl($scope, JobService, gridService, $state, ModalServ, NotifServ, swalService) {

        var vm = $scope;

        vm.selectedItem = {};

        vm.crear = crear;
        vm.listar = listar;
        vm.cambiarEstado = cambiarEstado;

        init();

        function init() {
            gridService.initGrid(vm);
            vm.gridOptions.rowTemplate = rowTemplate();
            listar();
        }

        function crear() {
            $state.go('job_form', {job_id: 0});
        }

        function listar() {
            var res = JobService.get(function () {
                if (res.estado === 200) {
                    vm.gridOptions.columnDefs = res.cols;
                    vm.gridOptions.data = res.items;
                }
            });
        }


        function rowTemplate() {    //custom rowtemplate to enable double click and right click menu options
            return '<div ng-dblclick="grid.appScope.rowDblClick(row)"  ng-repeat="(colRenderIndex, col) in colContainer.renderedColumns track by col.colDef.name" class="ui-grid-cell" ng-class="{ \'ui-grid-row-header-cell\': col.isRowHeader }"  ui-grid-cell></div>'
        }

        vm.rowDblClick = function (row) {
            vm.selectedItem = row.entity;
            showModalDetalles();
        }

        function showModalDetalles() {
            ModalServ.show('modalDetallesJob');
        }

        function hideModalDetalles() {
            ModalServ.hide('modalDetallesJob');
        }

        function cambiarEstado(estado) {
            swalService.confirm('¿Esta seguro?', function (confirm) {
                if (confirm) {
                    var params = {
                        job_id: vm.selectedItem.job_id,
                        newestado: estado
                    };
                    var res = JobService.cambiarEstado(params, function () {
                        if (res.estado === 200) {
                            NotifServ.success(res.msg);
                            hideModalDetalles();
                            listar();
                        }
                    });
                }
            }, 'Cambiar estado del pedido');
        }
    }
})();