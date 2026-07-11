你希望像使用 GitHub 那样使用 GitLab 的免费版，这完全没问题。GitLab 的免费 SaaS 版本（即 **GitLab.com**）对个人开发者非常友好，核心功能与 GitHub 免费版类似，甚至内置了 CI/CD。下面我带你一步步操作。

### 🧭 整体流程：从注册到使用

下图概括了从零开始使用 GitLab 免费版的主要步骤，你可以先有个整体概念：

<svg id="mmd-1783524997798-3" width="100%" xmlns="http://www.w3.org/2000/svg" class="flowchart" style="max-width: 100%; height: 100%; width: 100%; overflow: hidden; transform-origin: 0px 0px 0px; transform: matrix(1, 0, 0, 1, 0, 0);" viewBox="0 0 2041.862548828125 123" role="graphics-document document" aria-roledescription="flowchart-v2"><g><marker id="mmd-1783524997798-3_flowchart-v2-pointEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-pointStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="4.5" refY="5" markerUnits="userSpaceOnUse" markerWidth="8" markerHeight="8" orient="auto"><path d="M 0 5 L 10 10 L 10 0 z" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-pointEnd-margin" class="marker flowchart-v2" viewBox="0 0 11.5 14" refX="11.5" refY="7" markerUnits="userSpaceOnUse" markerWidth="10.5" markerHeight="14" orient="auto"><path d="M 0 0 L 11.5 7 L 0 14 z" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-pointStart-margin" class="marker flowchart-v2" viewBox="0 0 11.5 14" refX="1" refY="7" markerUnits="userSpaceOnUse" markerWidth="11.5" markerHeight="14" orient="auto"><polygon points="0,7 11.5,14 11.5,0" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></polygon></marker><marker id="mmd-1783524997798-3_flowchart-v2-circleEnd" class="marker flowchart-v2" viewBox="0 0 10 10" refX="11" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mmd-1783524997798-3_flowchart-v2-circleStart" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-1" refY="5" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 1; stroke-dasharray: 1, 0;"></circle></marker><marker id="mmd-1783524997798-3_flowchart-v2-circleEnd-margin" class="marker flowchart-v2" viewBox="0 0 10 10" refY="5" refX="12.25" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mmd-1783524997798-3_flowchart-v2-circleStart-margin" class="marker flowchart-v2" viewBox="0 0 10 10" refX="-2" refY="5" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="14" orient="auto"><circle cx="5" cy="5" r="5" class="arrowMarkerPath" style="stroke-width: 0; stroke-dasharray: 1, 0;"></circle></marker><marker id="mmd-1783524997798-3_flowchart-v2-crossEnd" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="12" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-crossStart" class="marker cross flowchart-v2" viewBox="0 0 11 11" refX="-1" refY="5.2" markerUnits="userSpaceOnUse" markerWidth="11" markerHeight="11" orient="auto"><path d="M 1,1 l 9,9 M 10,1 l -9,9" class="arrowMarkerPath" style="stroke-width: 2; stroke-dasharray: 1, 0;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-crossEnd-margin" class="marker cross flowchart-v2" viewBox="0 0 15 15" refX="17.7" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" class="arrowMarkerPath" style="stroke-width: 2.5;"></path></marker><marker id="mmd-1783524997798-3_flowchart-v2-crossStart-margin" class="marker cross flowchart-v2" viewBox="0 0 15 15" refX="-3.5" refY="7.5" markerUnits="userSpaceOnUse" markerWidth="12" markerHeight="12" orient="auto"><path d="M 1,1 L 14,14 M 1,14 L 14,1" class="arrowMarkerPath" style="stroke-width: 2.5; stroke-dasharray: 1, 0;"></path></marker><g class="root"><g class="clusters"></g><g class="edgePaths"><path d="M263.913,61.5L268.496,61.5C273.079,61.5,282.246,61.5,290.746,61.5C299.246,61.5,307.079,61.5,310.996,61.5L314.913,61.5" id="mmd-1783524997798-3-L_A_B_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_A_B_0" data-points="W3sieCI6MjYzLjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6MjkxLjQxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6MzE4LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path><path d="M504.913,61.5L509.496,61.5C514.079,61.5,523.246,61.5,531.746,61.5C540.246,61.5,548.079,61.5,551.996,61.5L555.913,61.5" id="mmd-1783524997798-3-L_B_C_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_B_C_0" data-points="W3sieCI6NTA0LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6NTMyLjQxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6NTU5LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path><path d="M829.913,61.5L834.496,61.5C839.079,61.5,848.246,61.5,856.746,61.5C865.246,61.5,873.079,61.5,876.996,61.5L880.913,61.5" id="mmd-1783524997798-3-L_C_D_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_C_D_0" data-points="W3sieCI6ODI5LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6ODU3LjQxMjUwNjEwMzUxNTYsInkiOjYxLjV9LHsieCI6ODg0LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path><path d="M1098.913,61.5L1103.496,61.5C1108.079,61.5,1117.246,61.5,1125.746,61.5C1134.246,61.5,1142.079,61.5,1145.996,61.5L1149.913,61.5" id="mmd-1783524997798-3-L_D_E_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_D_E_0" data-points="W3sieCI6MTA5OC45MTI1MDYxMDM1MTU2LCJ5Ijo2MS41fSx7IngiOjExMjYuNDEyNTA2MTAzNTE1NiwieSI6NjEuNX0seyJ4IjoxMTUzLjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path><path d="M1381.913,61.5L1386.496,61.5C1391.079,61.5,1400.246,61.5,1408.746,61.5C1417.246,61.5,1425.079,61.5,1428.996,61.5L1432.913,61.5" id="mmd-1783524997798-3-L_E_F_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_E_F_0" data-points="W3sieCI6MTM4MS45MTI1MDYxMDM1MTU2LCJ5Ijo2MS41fSx7IngiOjE0MDkuNDEyNTA2MTAzNTE1NiwieSI6NjEuNX0seyJ4IjoxNDM2LjkxMjUwNjEwMzUxNTYsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path><path d="M1690.863,61.5L1695.446,61.5C1700.029,61.5,1709.196,61.5,1717.696,61.5C1726.196,61.5,1734.029,61.5,1737.946,61.5L1741.863,61.5" id="mmd-1783524997798-3-L_F_G_0" class="edge-thickness-normal edge-pattern-solid edge-thickness-normal edge-pattern-solid flowchart-link" style=";" data-edge="true" data-et="edge" data-id="L_F_G_0" data-points="W3sieCI6MTY5MC44NjI1MDMwNTE3NTc4LCJ5Ijo2MS41fSx7IngiOjE3MTguMzYyNTAzMDUxNzU3OCwieSI6NjEuNX0seyJ4IjoxNzQ1Ljg2MjUwMzA1MTc1NzgsInkiOjYxLjV9XQ==" data-look="classic" marker-end="url(#mmd-1783524997798-3_flowchart-v2-pointEnd)"></path></g><g class="edgeLabels"><g class="edgeLabel"><g class="label" data-id="L_A_B_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_B_C_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_C_D_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_D_E_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_E_F_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g><g class="edgeLabel"><g class="label" data-id="L_F_G_0" transform="translate(0, 0)"><foreignObject width="0" height="4" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" class="labelBkg" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; background-color: rgba(241, 245, 249, 0.5); display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="edgeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175); background-color: rgb(241, 245, 249); text-align: center;"></span></div></foreignObject></g></g></g><g class="nodes"><g class="node default" id="mmd-1783524997798-3-flowchart-A-0" data-look="classic" transform="translate(135.9562530517578, 61.5)"><rect class="basic label-container" style="" x="-127.95625305175781" y="-32.5" width="255.91250610351562" height="65"></rect><g class="label" style="" transform="translate(-83.95625305175781, -10.5)"><rect></rect><foreignObject width="167.91250610351562" height="20" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">访问 GitLab.com 注册账号</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-B-1" data-look="classic" transform="translate(411.9125061035156, 61.5)"><rect class="basic label-container" style="" x="-93" y="-32.5" width="186" height="65"></rect><g class="label" style="" transform="translate(-49, -10.5)"><rect></rect><foreignObject width="98" height="20" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">验证邮箱并登录</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-C-3" data-look="classic" transform="translate(694.9125061035156, 61.5)"><rect class="basic label-container" style="" x="-135" y="-43" width="270" height="86"></rect><g class="label" style="" transform="translate(-91, -21)"><rect></rect><foreignObject width="182" height="34" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">配置 SSH 密钥<br>（推荐，便于安全推送代码）</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-D-5" data-look="classic" transform="translate(991.9125061035156, 61.5)"><rect class="basic label-container" style="" x="-107" y="-43" width="214" height="86"></rect><g class="label" style="" transform="translate(-63, -21)"><rect></rect><foreignObject width="126" height="34" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">创建新项目<br>（选择私有或公开）</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-E-7" data-look="classic" transform="translate(1267.9125061035156, 61.5)"><rect class="basic label-container" style="" x="-114" y="-43" width="228" height="86"></rect><g class="label" style="" transform="translate(-70, -21)"><rect></rect><foreignObject width="140" height="34" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">克隆仓库到本地<br>或直接在网页上传文件</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-F-9" data-look="classic" transform="translate(1563.8875045776367, 61.5)"><rect class="basic label-container" style="" x="-126.9749984741211" y="-43" width="253.9499969482422" height="86"></rect><g class="label" style="" transform="translate(-82.9749984741211, -21)"><rect></rect><foreignObject width="165.9499969482422" height="34" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: nowrap; line-height: 1; max-width: 200px; text-align: center; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">使用 Git 命令管理代码<br>（add / commit / push）</p></span></div></foreignObject></g></g><g class="node default" id="mmd-1783524997798-3-flowchart-G-11" data-look="classic" transform="translate(1889.8625030517578, 61.5)"><rect class="basic label-container" style="" x="-144" y="-53.5" width="288" height="107"></rect><g class="label" style="" transform="translate(-100, -31.5)"><rect></rect><foreignObject width="200" height="48" style="overflow: visible;"><div xmlns="http://www.w3.org/1999/xhtml" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; display: inline-block; white-space: break-spaces; line-height: 1; max-width: 200px; text-align: center; width: 200px; height: auto;"><span class="nodeLabel" style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline; fill: rgb(30, 64, 175); color: rgb(30, 64, 175);"><p style="margin: 0px; padding: 0px; border: 0px; font-size: 14px; vertical-align: baseline;">探索更多功能<br>（Issues, Merge Requests, CI/CD）</p></span></div></foreignObject></g></g></g></g></g><defs><filter id="mmd-1783524997798-3-drop-shadow" height="130%" width="130%"><feDropShadow dx="4" dy="4" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs><defs><filter id="mmd-1783524997798-3-drop-shadow-small" height="150%" width="150%"><feDropShadow dx="2" dy="2" stdDeviation="0" flood-opacity="0.06" flood-color="#000000"></feDropShadow></filter></defs><linearGradient id="mmd-1783524997798-3-gradient" gradientUnits="objectBoundingBox" x1="0%" y1="0%" x2="100%" y2="0%"></linearGradient></svg>

### 1️⃣ 注册与登录

1. **访问官网**：打开 [GitLab 官网](https://gitlab.com/)，点击右上角的 **“Register now”** 或 “Register”csdn.net+1。
2. **填写信息**：使用你的邮箱、用户名和密码进行注册。**用户名将成为你项目的默认命名空间**（例如 `gitlab.com/yourusername/your-project`），建议使用简洁的英文名csdn.net。
3. **验证邮箱**：注册后，GitLab 会发送一封验证邮件，点击邮件中的链接完成验证。
4. **登录**：使用注册的账号密码登录 GitLab。

> 💡 **小贴士**：登录后，建议立即在 **Settings → Preferences** 中开启 **Two-Factor Authentication (2FA)**，为你的账号增加一层安全保护csdn.net。

### 2️⃣ 配置 SSH 密钥（推荐）

配置 SSH 密钥可以让你在推送和拉取代码时无需反复输入用户名和密码，更安全便捷。这与 GitHub 的操作几乎一致。

1. **检查本地是否已有 SSH 密钥**：
   打开终端（Terminal、Git Bash 或 CMD），输入以下命令查看是否已有密钥：

```
    ls -al ~/.ssh
```

   如果看到 `id_rsa.pub` 或 `id_ed25519.pub` 文件，说明你已有公钥。

1. **生成新 SSH 密钥（若没有）**：
   如果没有，运行以下命令生成（替换为你的邮箱）：

```
    ssh-keygen -t ed25519 -C "your_email@example.com"
```

   一路回车即可（默认路径，密码可留空）csdn.net。

1. **复制公钥内容**：
   使用以下命令查看并复制公钥内容（`.pub` 文件）：

```
    cat ~/.ssh/id_ed25519.pub
```

1. **添加到 GitLab**：
   登录 GitLab，点击右上角头像 → **Preferences** → **SSH Keys**，将复制的公钥粘贴到输入框中，点击 **Add key**csdn.net。

### 3️⃣ 创建你的第一个项目

1. **新建项目**：
   登录后，在页面顶部或左侧导航栏找到并点击 **“New project”** 按钮informat.cn+1。
2. **选择创建方式**：
   选择 **“Create blank project”**（创建空白项目），这是最常用的方式jiandaoyun.com+1。
3. **填写项目信息**：
   - **Project name**：项目名称，将显示在项目主页。
   - **Project slug**：项目URL路径，通常自动生成，可自定义。
   - **Visibility Level**：**非常重要**，选择项目的可见性icode.best+1：
     - **Private**（私有）：只有你和你邀请的成员能访问。**个人项目常用**。
     - **Internal**（内部）：所有登录的 GitLab 用户可见（主要适用于企业内部实例）。
     - **Public**（公开）：任何人可见，**适合开源项目**。
   - 可选：添加项目描述，并勾选 **“Initialize repository with a README”** 来初始化一个 README 文件。
4. **创建项目**：
   点击 **“Create project”** 按钮，项目即创建成功informat.cn+1。

### 4️⃣ 将代码推送到 GitLab

你有两种主要方式将代码放入 GitLab 仓库。

#### 方法一：克隆仓库到本地（推荐用于现有项目）

1. **克隆仓库**：
   在项目主页，点击绿色的 **“Clone”** 按钮，复制 **SSH** 选项卡下的地址（例如 `git@gitlab.com:yourusername/your-project.git`）。
   在终端中，导航到你希望存放项目的目录，运行：

```
    git clone git@gitlab.com:yourusername/your-project.git
```

   这会创建一个与项目同名的文件夹tutorialspoint.com。

1. **添加文件并提交**：
   进入项目目录，将你的代码文件复制进去。然后使用 Git 命令跟踪和提交更改：

```
    cd your-project
    git add .
    git commit -m "Initial commit"
```

1. **推送更改到 GitLab**：
   第一次推送时，需要设置上游分支：

```
    git push -u origin master
```

   （如果你的主分支是 `main`，请将 `master` 替换为 `main`）tutorialspoint.com+1

#### 方法二：直接在网页上传文件（适合快速尝试）

1. 在项目主页，点击 **“Web IDE”** 按钮（或按键盘上的 `.` 键）打开在线编辑器icode.best。
2. 在左侧文件浏览器中，右键点击空白处，选择 **“Upload Files”**icode.best。
3. 选择你本地计算机的文件或文件夹（如果是文件夹，最好先压缩成 ZIP 再上传）上传。
4. 在弹出的提交信息框中填写描述，点击 **“Commit”** 提交。

### 5️⃣ 日常使用与协作

项目创建好后，你就可以像使用 GitHub 一样进行开发了。

- **管理代码**：使用 `git pull`（拉取最新代码）、`git add`、`git commit`、`git push` 等命令进行日常的代码同步和版本管理。
- **创建分支**：开发新功能或修复 Bug 时，建议创建分支：

```
    git checkout -b feature/new-login
    git push origin feature/new-login
```

- **发起合并请求**：
  在 GitLab 网页上，切换到你开发的分支，点击 **“Merge requests”** → **“New merge request”**，选择源分支和目标分支（通常是 `master` 或 `main`），填写描述并提交。这相当于 GitHub 的 Pull Request，用于代码审查和合并csdn.net。
- **问题追踪**：使用 **“Issues”** 功能来管理 Bug、任务和需求。你可以为 Issue 添加标签、指派负责人、关联里程碑等informat.cn+1。
- **尝试 CI/CD**：GitLab 的免费版包含**每月 400 分钟的 CI/CD 执行时长**（仅限 Linux Runner）javaguidepro.com。你只需在项目根目录创建一个 `.gitlab-ci.yml` 文件，定义构建、测试、部署的流程，GitLab 就会自动执行。这是 GitLab 相比 GitHub 免费版的一个显著优势。

### ⚠️ 注意事项与限制

作为免费用户，你需要了解以下限制，它们通常比 GitHub 免费版更宽松：



| 资源             | GitLab.com 免费版限制 | 说明                                                         |
| :--------------- | :-------------------- | :----------------------------------------------------------- |
| **私有仓库**     | **无限**              | 免费创建任意数量的私有仓库csdn.net。                         |
| **存储空间**     | **5GB / 命名空间**    | 你的所有项目（仓库、LFS大文件）总和不能超过 5GB。**注意**：此限制主要针对 GitLab.com SaaS 版。若自行部署社区版则无此限制gitlab.cn。 |
| **CI/CD 分钟数** | **400 分钟 / 月**     | 使用 GitLab 提供的共享 Runner 运行流水线的总时长。超出后需购买额外分钟数或使用自定义 Runner。**注意**：此限制仅针对 SaaS 版的共享 Runner。自行部署或使用自己的 Runner 则无此限制gitlab.cn+1。 |
| **项目成员数**   | 无限制                | 可以邀请无限多的成员到你的私有项目中协作。                   |

> 🚨 **重要提示**：上述 **5GB 存储限制和 400 分钟 CI/CD 限制是针对 GitLab.com SaaS 免费版** 的。如果你选择**自行部署 GitLab 社区版 (CE)**，则**没有这些限制**，但需要自己维护服务器gitlab.cn+1。

### ❓ 常见问题

<details> <summary><b>1. GitLab 免费版和 GitHub 免费版有什么主要区别？</b></summary> <br>

- **CI/CD**：GitLab 免费版**内置** CI/CD（每月400分钟），而 GitHub 需要使用 Actions 并自行配置。
- **私有仓库**：两者都免费提供无限私有仓库。
- **限制**：GitLab SaaS 版有存储和 CI/CD 分钟数限制，GitHub 免费版对协作者数量有限制（3人）。
- **定位**：GitLab 更侧重于**一体化 DevOps 平台**（内置 CI/CD、安全扫描等），GitHub 更侧重于**开源社区和代码托管**。

</details> <details> <summary><b>2. 如何查看我的存储和 CI/CD 用量？</b></summary> <br>

- **存储用量**：在顶部搜索栏搜索你的用户名或群组，进入其页面后，在左侧边栏选择 **Settings → Usage Quotas**，即可查看存储使用情况gitlab.cn。
- **CI/CD 分钟数**：同样在 **Usage Quotas** 页面，可以查看 CI/CD 分钟数的剩余额度。

</details> <details> <summary><b>3. 我可以导入我在 GitHub 上的项目吗？</b></summary> <br>

可以。在创建新项目时，选择 **“Import project”** 选项，然后选择从 GitHub 导入，按照提示授权即可informat.cn+1。

</details>

总而言之，**GitLab 的免费 SaaS 版本对于个人开发者来说功能足够强大，操作逻辑与 GitHub 高度相似**，你可以轻松上手。核心区别在于它内置了 CI/CD 并且对私有仓库的协作者人数没有限制，但需要注意其 SaaS 版本的存储和 CI/CD 时长限制。如果你主要进行个人项目或学习，GitLab.com 是一个非常好的选择。