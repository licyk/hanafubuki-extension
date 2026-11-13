# Hanafubuki extension registry

[简体中文](#简体中文)

The list of extensions that [Hanafubuki](https://github.com/licyk/Hanafubuki)'s
**Marketplace** (Settings > Extensions) shows and installs. Hanafubuki reads
[`extensions.json`](extensions.json) from this repository's `main` branch.

Being listed here does not mean an extension has been reviewed. Before
installing, Hanafubuki shows what the package asks for: its publisher, its
permissions, where it comes from and its SHA-256.

## The format

```json
{
  "schema": 1,
  "extensions": [
    {
      "id": "com.example.greeter",
      "name": { "en": "Greeter", "zh": "问候" },
      "author": "Example",
      "description": { "en": "Greets you.", "zh": "向你问好。" },
      "reference": "https://github.com/example/greeter",
      "download_url": "https://github.com/example/greeter/releases/download/v1.0.0/com.example.greeter-1.0.0.zip",
      "update_url": "https://github.com/example/greeter/releases/latest/download/latest.json"
    }
  ]
}
```

| Field | Required | Meaning |
| --- | --- | --- |
| `id` | yes | The `id` of the extension's manifest (`hanafubuki-extension.toml`): reverse-DNS, two or more labels of `[a-z0-9-]` joined by dots. A package installed from this entry must have this id. |
| `name` | yes | Text, or an object of language to text (`en`, `zh`, …). |
| `author` | yes | The author's name. |
| `reference` | yes | The source repository's URL. |
| `description` | no | Text, or an object of language to text. |
| `download_url` | no | An archive Hanafubuki installs: `.zip`, `.tar`, `.tar.gz`, `.tar.xz` or `.tar.bz2`, usually attached to a GitHub release. |
| `update_url` | no | The extension's `latest.json`, the same file its manifest's `[update] url` names. |

- **Installing:** Hanafubuki installs from `update_url` when there is one,
  taking the entry for the user's platform and checking its `sha256`, so it
  always gets the newest version. Otherwise it installs `download_url`.
- **Neither URL:** an entry with no `update_url` and no `download_url` is
  listed with its source link only.
- **Unknown fields** are ignored.
- **A broken entry**, one missing a required field or naming an id already
  listed, is skipped. The others still show.

## Adding an extension

1. Fork this repository and add your entry to `extensions.json`. Keep the
   entries sorted by `id`.
2. Run `python scripts/check.py`, which needs only the standard library.
3. Open a pull request. The same check runs on it.

A release's `latest.json` lists its packages:

```json
[
  {
    "version": "1.0.0",
    "download_url": "https://…/com.example.greeter-1.0.0.zip",
    "sha256": "…",
    "platform": "any",
    "architecture": "any"
  }
]
```

`platform` is `windows`, `linux`, `macos` or `any`. `architecture` is
`x86_64`, `aarch64` or `any`. See the
[extension author's guide](https://hanafubuki.netlify.app/en/docs/extension-dev)
for packaging and updates.

`schema/extensions.schema.json` is the JSON Schema of the format, for
editors.

## 简体中文

[Hanafubuki](https://github.com/licyk/Hanafubuki) 的**扩展市场**（设置 > 扩展）中显示和安装的扩展列表。Hanafubuki 读取本仓库 `main` 分支的 [`extensions.json`](extensions.json)。

列在这里不代表扩展经过审核。安装前，Hanafubuki 会显示软件包的发布者、所需权限、来源和 SHA-256。

### 格式

| 字段 | 必填 | 含义 |
| --- | --- | --- |
| `id` | 是 | 扩展清单（`hanafubuki-extension.toml`）中的 `id`：反向域名格式，由点连接的两个或更多 `[a-z0-9-]` 标签。从该条目安装的软件包必须使用此 id。 |
| `name` | 是 | 文本，或语言到文本的对象（`en`、`zh` 等）。 |
| `author` | 是 | 作者名称。 |
| `reference` | 是 | 源代码仓库的 URL。 |
| `description` | 否 | 文本，或语言到文本的对象。 |
| `download_url` | 否 | Hanafubuki 安装的压缩包：`.zip`、`.tar`、`.tar.gz`、`.tar.xz` 或 `.tar.bz2`，通常附在 GitHub Release 中。 |
| `update_url` | 否 | 扩展的 `latest.json`，即清单中 `[update] url` 指向的文件。 |

- **安装：** 有 `update_url` 时，Hanafubuki 从它安装：选取适用于用户平台的条目并校验其 `sha256`，因此总能得到最新版本。否则安装 `download_url`。
- **两个 URL 都没有：** 这样的条目只显示源代码链接。
- **未知字段**会被忽略。
- **有问题的条目**（缺少必填字段，或 id 已被列出）会被跳过，其余条目照常显示。

### 添加扩展

1. Fork 本仓库，在 `extensions.json` 中添加你的条目，并保持条目按 `id` 排序。
2. 运行 `python scripts/check.py`（只需要标准库）。
3. 提交 Pull Request，同样的检查会在其上运行。

打包与更新见[扩展开发指南](https://hanafubuki.netlify.app/docs/extension-dev)。
