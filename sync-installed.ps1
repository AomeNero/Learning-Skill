# sync-installed.ps1 —— 把本仓库的 skills/ 与 agents/ 全量同步到 Claude Code 已装目录（~/.claude/）
#
# 仓库是唯一事实源。只触碰仓库内同名技能/代理目录，绝不影响其他已装内容；
# 同名目录内做镜像（复制更新 + 清理仓库里已删除的文件）。
# 从仓库删除整个技能不会删已装副本——下线技能请手动清理。
#
# 用法：powershell -File .\sync-installed.ps1（或在仓库根目录 .\sync-installed.ps1）

$ErrorActionPreference = "Stop"
$repo   = $PSScriptRoot
$target = Join-Path $HOME ".claude"
$groups = @("skills", "agents")

foreach ($g in $groups) {
    $srcRoot = Join-Path $repo $g
    $dstRoot = Join-Path $target $g
    if (-not (Test-Path $srcRoot)) { Write-Warning "仓库缺少 $g/，跳过"; continue }
    if (-not (Test-Path $dstRoot)) { New-Item -ItemType Directory -Force $dstRoot | Out-Null }

    Get-ChildItem $srcRoot | ForEach-Object {
        $name = $_.Name

        # 散文件（如 agents/*.md）：直接覆盖复制；仓库里删掉的文件不主动删已装副本
        if (-not $_.PSIsContainer) {
            Copy-Item $_.FullName -Destination $dstRoot -Force
            Write-Host "同步: $g/$name -> ~/$g/$name"
            return
        }

        # 目录（如 skills/learning）：镜像同步——复制更新 + 清理仓库里已删除的文件与空目录
        $src = $_.FullName
        $dst = Join-Path $dstRoot $name
        New-Item -ItemType Directory -Force $dst | Out-Null

        Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force

        Get-ChildItem $dst -Recurse -File | ForEach-Object {
            $rel = $_.FullName.Substring($dst.Length).TrimStart("\")
            if (-not (Test-Path (Join-Path $src $rel))) {
                Remove-Item $_.FullName -Force
                Write-Host "  清理（仓库已无）: $g/$name/$rel"
            }
        }
        Get-ChildItem $dst -Recurse -Directory |
            Sort-Object { $_.FullName.Length } -Descending |
            Where-Object { -not (Get-ChildItem $_.FullName -Recurse -File) } |
            ForEach-Object {
                Write-Host "  清理空目录: $g/$name/$($_.FullName.Substring($dst.Length).TrimStart('\'))"
                Remove-Item $_.FullName -Force
            }

        Write-Host "同步: $g/$name -> ~/$g/$name"
    }
}

Write-Host "`n完成——本仓库 skills/ 与 agents/ 已同步到 $target"
