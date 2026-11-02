/**
 * 解析字典列表数据（兼容 response, response.data 以及 response.data.data）
 */
export function parseDictData(res: any): any[] {
    if (!res) return [];
    if (Array.isArray(res)) return res;
    if (Array.isArray(res.data)) return res.data;
    if (Array.isArray(res.data?.data)) return res.data.data;
    return [];
}

/**
 * 回显数据字典标签
 * @param datas 字典数组或包含数组的对象
 * @param value 字典值
 * @returns 字典标签
 */
export function selectDictLabel(datas: any, value: any): string {
    if (!datas || value === undefined || value === null) return '';
    const list = parseDictData(datas);
    const target = list.find((item: any) => {
        const val = item.dict_value !== undefined ? item.dict_value : item.dictValue;
        return String(val) === String(value);
    });
    if (!target) return '';
    return target.dict_label !== undefined ? target.dict_label : (target.dictLabel || '');
}

/**
 * 通用下载方法
 */
export function download(fileName: string) {
    const baseURL = (import.meta.env.VITE_API_URL as string) || '';
    const url = baseURL.endsWith('/') ? baseURL : `${baseURL}/`;
    window.location.href = `${url}common/download?fileName=${encodeURI(fileName)}&delete=true`;
}
