// 递归/字典法: 将列表数据转换成树形数据
export function toArrayTree(list: any[]) {
    if (!Array.isArray(list)) return [];
    const treeList: any[] = [];
    const map: Record<string | number, any> = {};
    // 遍历list数组，加入map对象，id作为key，初始化children
    list.forEach((item: any) => {
        map[item.id] = item;
        item.children = [];
    });
    // 再次遍历list数组，匹配parent
    list.forEach((item: any) => {
        if (item.parent && map[item.parent]) {
            map[item.parent].children.push(item);
        } else {
            treeList.push(item);
        }
    });
    return treeList;
}