import numpy as np
import matplotlib.pyplot as plt

def dtlz1(x, M=2):
    """
    An implementation of the DTLZ1 test problem. M is the number of objectives (2 by default, override for 3).
    """
    z = x[M-1:] - 0.5
    gp1 = 100 * (x[M-1:].shape[0] + np.dot(z, z) - np.cos(20 * np.pi * z).sum()) + 1
    f = np.array([gp1] * M)

    f[0] *= 0.5 * np.prod(x[0:M-1])
    for i in range(1, M-1):
        f[i] *= 0.5 * np.prod(x[0:M-i-1]) * (1 - x[M-i-1])
    f[M-1] *= 0.5 * (1 - x[0])

    return f


def dtlz2(x, M=2):
    """
    An implementation of the DTLZ2 test problem. M is the number of objectives (2 by default, override for 3).
    """
    gp1 = ((x[M-1:] - 0.5)**2).sum() + 1
    f = np.array([gp1] * M)

    for i in range(M):
        if M-i-1 > 0:
            for j in range(M-i-1):
                f[i] *= np.cos((np.pi * x[j]) / 2)

        if i > 0:
            f[i] *= np.sin((np.pi * x[M-i-1]) / 2)

    return f

def dominates(u, v):
    return (u<=v).all() and (u<v).any()

#DTLZ1 2 objectives, 6 decision variables

n = 500
x = np.random.rand(n, 6)
y = np.array([dtlz1(X) for X in x])

plt.ion()
plt.scatter(y[:,0], y[:,1], marker="x")

archive = []

for i in x:
    dominated = False
    for j in x:
        if dominates(dtlz1(j), dtlz1(i)):
            dominated = True
            break
    if not dominated:
        archive.append(i)

for i in range(500):
    parent = np.array(archive[np.random.randint(len(archive))])

    ajust = parent[np.random.randint(len(parent))] + 0.2 * np.random.randn()

    if ajust < 0:
        ajust = 0.0
    elif ajust > 1:
        ajust = 1.0

    parent[np.random.randint(len(parent))] = ajust

    dominated = False

    for j in archive:
        if dominates(dtlz1(j), dtlz1(parent)):
            dominated = True

    if not dominated:
        newarchive = []
        for j in archive:
            if not dominates(dtlz1(parent), dtlz1(j)):
                newarchive.append(j)
        archive = newarchive
        archive.append(parent)

archive = np.array(archive)

front = np.array([dtlz1(X) for X in archive])

plt.scatter(front[:,0], front[:,1], marker="D")
    
plt.title("%d Random solutions to DTLZ1" % n)
plt.xlabel("$f_1$")
plt.ylabel("$f_2$")
plt.show()

#DTLZ1 3 objectives 7 decision variables

n = 500
x = np.random.rand(n, 7)
y = np.array([dtlz1(X, M=3) for X in x])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(y[:,0], y[:,1], y[:,2], marker="x")

archive = []

for i in x:
    dominated = False
    for j in x:
        if dominates(dtlz1(j, M=3), dtlz1(i, M=3)):
            dominated = True
            break
    if not dominated:
        archive.append(i)

for i in range(500):
    parent = np.array(archive[np.random.randint(len(archive))])

    ajust = parent[np.random.randint(len(parent))] + 0.2 * np.random.randn()

    if ajust < 0:
        ajust = 0.0
    elif ajust > 1:
        ajust = 1.0

    parent[np.random.randint(len(parent))] = ajust

    dominated = False

    for j in archive:
        if dominates(dtlz1(j, M=3), dtlz1(parent, M=3)):
            dominated = True

    if not dominated:
        newarchive = []
        for j in archive:
            if not dominates(dtlz1(parent, M=3), dtlz1(j, M=3)):
                newarchive.append(j)
        archive = newarchive
        archive.append(parent)

archive = np.array(archive)

front = np.array([dtlz1(X, M=3) for X in archive])

ax.scatter(front[:,0], front[:,1], front[:,2], marker="D")

ax.set_xlabel('$f_1$')
ax.set_ylabel('$f_2$')
ax.set_zlabel('$f_3$')
ax.set_title("500 Random solutions to DTLZ1 (3 objectives)")

plt.show()

#DTLZ2 2 objectives 11 decision variables

n = 500
x = np.random.rand(n, 11)
y = np.array([dtlz2(X) for X in x])

plt.figure()
plt.ion()
plt.scatter(y[:,0], y[:,1])

archive = []

for i in x:
    dominated = False
    for j in x:
        if dominates(dtlz2(j), dtlz2(i)):
            dominated = True
            break
    if not dominated:
        archive.append(i)

for i in range(500):
    parent = np.array(archive[np.random.randint(len(archive))])

    ajust = parent[np.random.randint(len(parent))] + 0.2 * np.random.randn()

    if ajust < 0:
        ajust = 0.0
    elif ajust > 1:
        ajust = 1.0

    parent[np.random.randint(len(parent))] = ajust

    dominated = False

    for j in archive:
        if dominates(dtlz2(j), dtlz2(parent)):
            dominated = True

    if not dominated:
        newarchive = []
        for j in archive:
            if not dominates(dtlz2(parent), dtlz2(j)):
                newarchive.append(j)
        archive = newarchive
        archive.append(parent)

archive = np.array(archive)

front = np.array([dtlz2(X) for X in archive])

plt.scatter(front[:,0], front[:,1], marker="D")

plt.title("%d Random solutions to DTLZ2" % n)
plt.xlabel("$f_1$")
plt.ylabel("$f_2$")
plt.show()

#DTLZ2 3 objectives 12 decision variables

n = 500
x = np.random.rand(n, 12)
y = np.array([dtlz2(X, M=3) for X in x])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(y[:,0], y[:,1], y[:,2])

archive = []

for i in x:
    dominated = False
    for j in x:
        if dominates(dtlz2(j, M=3), dtlz2(i, M=3)):
            dominated = True
            break
    if not dominated:
        archive.append(i)

for i in range(500):
    parent = np.array(archive[np.random.randint(len(archive))])

    ajust = parent[np.random.randint(len(parent))] + 0.2 * np.random.randn()

    if ajust < 0:
        ajust = 0.0
    elif ajust > 1:
        ajust = 1.0

    parent[np.random.randint(len(parent))] = ajust

    dominated = False

    for j in archive:
        if dominates(dtlz2(j, M=3), dtlz2(parent, M=3)):
            dominated = True

    if not dominated:
        newarchive = []
        for j in archive:
            if not dominates(dtlz2(parent, M=3), dtlz2(j, M=3)):
                newarchive.append(j)
        archive = newarchive
        archive.append(parent)

archive = np.array(archive)

front = np.array([dtlz2(X, M=3) for X in archive])

ax.scatter(front[:,0], front[:,1], front[:,2], marker="D")

ax.set_xlabel('$f_1$')
ax.set_ylabel('$f_2$')
ax.set_zlabel('$f_3$')
ax.set_title("500 Random solutions to DTLZ2 (3 objectives)")

plt.show()
