# 线段树

线段树是算法竞赛中常用的用来维护 **区间信息** 的数据结构。

线段树可以在 $O(\log N)$ 的时间复杂度内实现单点修改、区间修改、区间查询（区间求和，求区间最大值，求区间最小值）等操作。

线段树维护的信息，需要满足可加性，即能以可以接受的速度合并信息和修改信息，包括在使用懒惰标记时，标记也要满足可加性（例如取模就不满足可加性，对 $4$ 取模然后对 $3$ 取模，两个操作就不能合并在一起做）。

## simplest from of a segment tree



We have an array a[0…n−1], 

and the Segment Tree must be able to find the sum of elements between the indices l and r (i.e. computing the sum $∑_{ri}^l= a[i]$)

<img src="https://raw.githubusercontent.com/e-maxx-eng/e-maxx-eng/master/img/sum-segment-tree.png" alt="&quot;Sum Segment Tree&quot;" style="zoom: 67%;" />

### Counstruction

from the root vertex to the leaf vertices.  does the following:



1. recursively construct the values of the two child vertices 递归地构造两个子顶点的值
2. merge the computed values of these children.合并这些子节点的计算值

The time complexity of this construction is O(n),



```c
int n, t[4*MAXN];
void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = a[tl];
    } else {
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        t[v] = t[v*2] + t[v*2+1];
    }
}
```

So, we store the Segment Tree simply as an array t[] with a size of 4 times the input size n:

### Sum queries

There are three possible cases.

1.The easiest case is when the segment a[l…r] is equal to the corresponding segment of the current vertex (i.e. a[l…r]=a[tl…tr]).then we are finished and can return the precomputed sum that is stored in the vertex.

2.the segment of the query can fall completely into the domain of either the left or the right child.

3.And then there is the last case, the query segment intersects with both children. In this case we have no other option as to make two recursive calls, one for each child. First we go to the left child, compute a partial answer for this vertex (i.e. the sum of values of the intersection between the segment of the query and the segment of the left child), then go to the right child, compute the partial answer using that vertex, and then combine the answers by adding them.

So processing a sum query is a function that recursively calls

And the recursion ends, whenever the boundaries of the current query segment coincides with the boundaries of the segment of the current vertex



##### complexity of this algorithm O(logn)





The procedure is illustrated in the following image. 该过程如下图所示

Again the array a=[1,3,−2,8,−7] is used, and here we want to compute the sum $∑_{i=2}^4a[i]$. The colored 彩色vertices will be visited, and we will use the precomputed values of the green vertices. This gives us the result −2+1=−1.

!["Sum Segment Tree Query"](https://raw.githubusercontent.com/e-maxx-eng/e-maxx-eng/master/img/sum-segment-tree-query.png)

```c
int sum(int v, int tl, int tr, int l, int r) { //i.e. the index v and the boundaries tl and tr information about the boundaries of the query, l and r
    if (l > r) 
        return 0;
    if (l == tl && r == tr) {
        return t[v];
    }
    int tm = (tl + tr) / 2;
    return sum(v*2, tl, tm, l, min(r, tm))
           + sum(v*2+1, tm+1, tr, max(l, tm+1), r);
}
```

### Update queries

#### problem:Now we want to modify a specific element in the array

let's say we want to do the assignment a[i]=x



It is easy to see, that the update request can be implemented using a recursive function. The function gets passed the current tree vertex, and it recursively calls itself with one of the two child vertices (the one that contains a[i] in its segment), and after that recomputes its sum value

Again here is using the same array. Here we perform the update a[2]=3. The green vertices are the vertices that we visit and update.

!["Sum Segment Tree Update"](https://raw.githubusercontent.com/e-maxx-eng/e-maxx-eng/master/img/sum-segment-tree-update.png)

```c
void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        t[v] = new_val;
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
        t[v] = t[v*2] + t[v*2+1];
    }
}
```

## Advanced versions of Segment Trees

#### Finding the maximum

The tree will have exactly the same structure as the tree described above. 

We only need to change the way t[v] is computed in the build and update functions. t[v] will now store the maximum of the corresponding segment. And we also need to change the calculation of the returned value of the sum function (replacing the summation by the maximum).

#### Finding the maximum and the number of times it appears

#### problem ：findind the maximum

we store a pair of numbers at each vertex in the tree: In addition to the maximum we also store the number of occurrences of it in the corresponding segment. Determining the correct pair to store at t[v] can still be done in constant time using the information of the pairs stored at the child vertices. 

Combining two such pairs should be done in a separate function, since this will be an operation that we will do while building the tree, while answering maximum queries and while performing modifications.

```c
pair<int, int> t[4*MAXN];

pair<int, int> combine(pair<int, int> a, pair<int, int> b) {
    if (a.first > b.first) 
        return a;
    if (b.first > a.first)
        return b;
    return make_pair(a.first, a.second + b.second);
}

void build(int a[], int v, int tl, int tr) {
    if (tl == tr) {
        t[v] = make_pair(a[tl], 1);
    } else {
        int tm = (tl + tr) / 2;
        build(a, v*2, tl, tm);
        build(a, v*2+1, tm+1, tr);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}

pair<int, int> get_max(int v, int tl, int tr, int l, int r) {
    if (l > r)
        return make_pair(-INF, 0);
    if (l == tl && r == tr)
        return t[v];
    int tm = (tl + tr) / 2;
    return combine(get_max(v*2, tl, tm, l, min(r, tm)), 
                   get_max(v*2+1, tm+1, tr, max(l, tm+1), r));
}

void update(int v, int tl, int tr, int pos, int new_val) {
    if (tl == tr) {
        t[v] = make_pair(new_val, 1);
    } else {
        int tm = (tl + tr) / 2;
        if (pos <= tm)
            update(v*2, tl, tm, pos, new_val);
        else
            update(v*2+1, tm+1, tr, pos, new_val);
        t[v] = combine(t[v*2], t[v*2+1]);
    }
}
```

#### Compute the greatest common divisor / least common multiple

#### problem：compute gcd/lcm 最大公约数/最小公倍数 

#### in this problem, we want to compute the GCD / LCM of all numbers of given ranges of the array.

To do this task, we will descend the Segment Tree, starting at the root vertex, and moving each time to either the left or the right child, depending on which segment contains the k-th zero. In order to decide to which child we need to go, it is enough to look at the number of zeros appearing in the segment corresponding to the left vertex. If this precomputed count is greater or equal to k, it is necessary to descend to the left child, and otherwise descent to the right child. Notice, if we chose the right child, we have to subtract the number of zeros of the left child from k.

```c
int find_kth(int v, int tl, int tr, int k) {
    if (k > t[v])
        return -1;
    if (tl == tr)
        return tl;
    int tm = (tl + tr) / 2;
    if (t[v*2] >= k)
        return find_kth(v*2, tl, tm, k);
    else 
        return find_kth(v*2+1, tm+1, tr, k - t[v*2]);
}
```

#### Searching for the first element greater than a given amount

#### problem：The task is as follows: for a given value xx and a range a[l…r] find the smallest ii in the range a[l…r], such that a[i] is greater than x.

```c
int get_first(int v, int lv, int rv, int l, int r, int x) {
    if(lv > r || rv < l) return -1;
    if(l <= lv && rv <= r) {
        if(t[v] <= x) return -1;
        while(lv != rv) {
            int mid = lv + (rv-lv)/2;
            if(t[2*v] > x) {
                v = 2*v;
                rv = mid;
            }else {
                v = 2*v+1;
                lv = mid+1;
            }
        }
        return lv;
    }

    int mid = lv + (rv-lv)/2;
    int rs = get_first(2*v, lv, mid, l, r, x);
    if(rs != -1) return rs;
    return get_first(2*v+1, mid+1, rv, l ,r, x);
}
```

### Generalization to higher dimensions   **对更高维度的推广**

A matrix a[0…n−1,0…m−1] is given, and we have to find the sum (or minimum/maximum) on some submatrix a[x1…x2,y1…y2], as well as perform modifications of individual单个 matrix elements (i.e. queries of the form a[x][y]=p).

Here is the implementation of the construction of a 2D Segment Tree. It actually represents代表 two separate分开 blocks: the construction of a Segment Tree along the x coordinate （x 坐标） (buildx), and the y coordinate (buildy). For the leaf nodes in buildy we have to separate two cases:我们必须分离两种情况:  when the current segment of the first coordinate [tlx…trx] has length 1,当第一个坐标[ tlx... trx ]的当前段长度为1时，以及当它的长度大于1时 and when it has a length greater than one. In the first case, we just take the corresponding value from the matrix, and in the second case we can combine the values of two Segment Trees from the left and the right son in the coordinate x.我们只需要从矩阵中取得相应的值，在第二种情况下，我们可以在坐标 x 中合并两个从左边和右边的段树的值。

```c
void build_y(int vx, int lx, int rx, int vy, int ly, int ry) {
    if (ly == ry) {
        if (lx == rx)
            t[vx][vy] = a[lx][ly];
        else
            t[vx][vy] = t[vx*2][vy] + t[vx*2+1][vy];
    } else {
        int my = (ly + ry) / 2;
        build_y(vx, lx, rx, vy*2, ly, my);
        build_y(vx, lx, rx, vy*2+1, my+1, ry);
        t[vx][vy] = t[vx][vy*2] + t[vx][vy*2+1];
    }
}

void build_x(int vx, int lx, int rx) {
    if (lx != rx) {
        int mx = (lx + rx) / 2;
        build_x(vx*2, lx, mx);
        build_x(vx*2+1, mx+1, rx);
    }
    build_y(vx, lx, rx, 1, 0, m-1);
}


```

```c
int sum_y(int vx, int vy, int tly, int try_, int ly, int ry) {
    if (ly > ry) 
        return 0;
    if (ly == tly && try_ == ry)
        return t[vx][vy];
    int tmy = (tly + try_) / 2;
    return sum_y(vx, vy*2, tly, tmy, ly, min(ry, tmy))
         + sum_y(vx, vy*2+1, tmy+1, try_, max(ly, tmy+1), ry);
}

int sum_x(int vx, int tlx, int trx, int lx, int rx, int ly, int ry) {
    if (lx > rx)
        return 0;
    if (lx == tlx && trx == rx)
        return sum_y(vx, 1, 0, m-1, ly, ry);
    int tmx = (tlx + trx) / 2;
    return sum_x(vx*2, tlx, tmx, lx, min(rx, tmx), ly, ry)
         + sum_x(vx*2+1, tmx+1, trx, max(lx, tmx+1), rx, ly, ry);
}
```

this fountion work in  O(logn logm)

#### Update

```c
void update_y(int vx, int lx, int rx, int vy, int ly, int ry, int x, int y, int new_val) {
    if (ly == ry) {
        if (lx == rx)
            t[vx][vy] = new_val;
        else
            t[vx][vy] = t[vx*2][vy] + t[vx*2+1][vy];
    } else {
        int my = (ly + ry) / 2;
        if (y <= my)
            update_y(vx, lx, rx, vy*2, ly, my, x, y, new_val);
        else
            update_y(vx, lx, rx, vy*2+1, my+1, ry, x, y, new_val);
        t[vx][vy] = t[vx][vy*2] + t[vx][vy*2+1];
    }
}

void update_x(int vx, int lx, int rx, int x, int y, int new_val) {
    if (lx != rx) {
        int mx = (lx + rx) / 2;
        if (x <= mx)
            update_x(vx*2, lx, mx, x, y, new_val);
        else
            update_x(vx*2+1, mx+1, rx, x, y, new_val);
    }
    update_y(vx, lx, rx, 1, 0, m-1, x, y, new_val);
}
```

### Preserving the history of its values (Persistent Segment Tree) 持久化线段树

```c
struct Vertex {
    Vertex *l, *r;
    int sum;

    Vertex(int val) : l(nullptr), r(nullptr), sum(val) {}
    Vertex(Vertex *l, Vertex *r) : l(l), r(r), sum(0) {
        if (l) sum += l->sum;
        if (r) sum += r->sum;
    }
};

Vertex* build(int a[], int tl, int tr) {
    if (tl == tr)
        return new Vertex(a[tl]);
    int tm = (tl + tr) / 2;
    return new Vertex(build(a, tl, tm), build(a, tm+1, tr));
}

int get_sum(Vertex* v, int tl, int tr, int l, int r) {
    if (l > r)
        return 0;
    if (l == tl && tr == r)
        return v->sum;
    int tm = (tl + tr) / 2;
    return get_sum(v->l, tl, tm, l, min(r, tm))
         + get_sum(v->r, tm+1, tr, max(l, tm+1), r);
}

Vertex* update(Vertex* v, int tl, int tr, int pos, int new_val) {
    if (tl == tr)
        return new Vertex(new_val);
    int tm = (tl + tr) / 2;
    if (pos <= tm)
        return new Vertex(update(v->l, tl, tm, pos, new_val), v->r);
    else
        return new Vertex(v->l, update(v->r, tm+1, tr, pos, new_val));
}
```

