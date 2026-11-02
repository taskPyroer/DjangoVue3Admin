import { ref, reactive, computed } from 'vue';
import { ElMessageBox, ElMessage } from 'element-plus';
import { handleFileError } from '@/utils/export';

export interface UseCrudOptions<T = any> {
    /** 查询列表的 API 函数 */
    listApi: (params: any) => Promise<any>;
    /** 删除项的 API 函数 */
    deleteApi?: (id: any) => Promise<any>;
    /** 导出 Excel 的 API 函数 */
    exportApi?: () => Promise<any>;
    /** 默认查询参数 */
    defaultParams?: Record<string, any>;
    /** 导出文件名默认前缀 */
    exportPrefix?: string;
    /** 业务名称（用于删除弹窗提示，如“岗位”） */
    title?: string;
    /** 数据后处理函数（如树形转换 toArrayTree） */
    transformData?: (data: any[]) => any[];
}

function getRowId(item: any): string | number | undefined {
    if (!item || typeof item !== 'object') return item;
    return item.id ?? item.ossId ?? item.mailId ?? item.configId ?? item.dictId ?? item.roleId ?? item.postId ?? item.infoId ?? item.operId ?? item.jobId ?? item.fileId;
}

export function useCrud<T = any>(options: UseCrudOptions<T>) {
    const {
        listApi,
        deleteApi,
        exportApi,
        defaultParams = {},
        exportPrefix = '数据导出',
        title = '数据项',
        transformData,
    } = options;

    const loading = ref(false);
    const tableData = ref<T[]>([]);
    const total = ref(0);
    const selectedRows = ref<T[]>([]);
    const selectedIds = ref<(string | number)[]>([]);

    const single = computed(() => selectedIds.value.length !== 1);
    const multiple = computed(() => selectedIds.value.length === 0);

    const queryParams = reactive<Record<string, any>>({
        page: 1,
        pageSize: 10,
        ...defaultParams,
    });

    /** 执行列表查询 */
    const handleQuery = async () => {
        loading.value = true;
        try {
            const res = await listApi(queryParams);
            const resData = res?.data;
            if (Array.isArray(resData?.data)) {
                tableData.value = transformData ? transformData(resData.data) : resData.data;
                total.value = Number(resData.total ?? resData.count ?? 0);
            } else if (Array.isArray(resData)) {
                tableData.value = transformData ? transformData(resData) : resData;
                total.value = Number(res?.total ?? res?.count ?? resData.length);
            } else {
                tableData.value = [];
                total.value = 0;
            }
        } catch (error) {
            console.error(`[useCrud] 查询失败:`, error);
        } finally {
            loading.value = false;
        }
    };

    /** 重置查询参数 */
    const resetQuery = (customReset?: () => void) => {
        if (customReset) {
            customReset();
        } else {
            Object.keys(defaultParams).forEach((key) => {
                queryParams[key] = defaultParams[key];
            });
            queryParams.page = 1;
            queryParams.pageSize = 10;
        }
        handleQuery();
    };

    /** 页码切换 */
    const handleCurrentChange = (val: number) => {
        queryParams.page = val;
        handleQuery();
    };

    /** 每页条数切换 */
    const handleSizeChange = (val: number) => {
        queryParams.pageSize = val;
        queryParams.page = 1;
        handleQuery();
    };

    /** 多选表格行变更 */
    const handleSelectionChange = (selection: T[]) => {
        selectedRows.value = selection;
        selectedIds.value = selection
            .map(getRowId)
            .filter((v): v is string | number => v !== undefined && v !== null);
    };

    /** 删除单项或批量删除 */
    const handleDelete = async (row?: any) => {
        if (!deleteApi) {
            console.warn(`[useCrud] 未提供 deleteApi`);
            return;
        }
        const rowId = getRowId(row);
        const targetIds = rowId ?? (selectedIds.value.length === 1 ? selectedIds.value[0] : selectedIds.value);
        if (!targetIds || (Array.isArray(targetIds) && targetIds.length === 0)) {
            ElMessage.warning('请选择需要删除的数据项');
            return;
        }

        const targetLabel = row?.dept_name ?? row?.name ?? row?.role_name ?? row?.configName ?? targetIds;
        const confirmText = `是否确认删除${title}为 "${targetLabel}" 的数据项?`;
        try {
            await ElMessageBox.confirm(confirmText, '警告', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            });
            await deleteApi(targetIds);
            ElMessage.success('删除成功');
            // 如果删除的是最后一页的唯一一条数据，自动回退上一页
            if (tableData.value.length === 1 && queryParams.page > 1) {
                queryParams.page -= 1;
            }
            await handleQuery();
        } catch (action) {
            // 取消无需提示
        }
    };

    /** 导出 Excel */
    const handleExport = async (customName?: string) => {
        if (!exportApi) {
            console.warn(`[useCrud] 未提供 exportApi`);
            return;
        }
        try {
            await ElMessageBox.confirm('是否确认导出所有数据项?', '警告', {
                confirmButtonText: '确定',
                cancelButtonText: '取消',
                type: 'warning',
            });
            const res = await exportApi();
            const timestamp = Math.floor(Date.now() / 1000);
            const fileName = `${customName || exportPrefix}_${timestamp}.xls`;
            handleFileError(res, fileName);
        } catch (action) {
            // 取消无需提示
        }
    };

    return {
        loading,
        tableData,
        total,
        queryParams,
        selectedRows,
        selectedIds,
        single,
        multiple,
        handleQuery,
        resetQuery,
        handleCurrentChange,
        handleSizeChange,
        handleSelectionChange,
        handleDelete,
        handleExport,
    };
}
