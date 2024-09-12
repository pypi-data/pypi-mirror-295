
from cerrax import DotDict


class UnicodeChars:

	VERSION='15.0' # This is the version of the Unicode standard applied here

	line = DotDict(
		solid = DotDict(
			horizontal = '\u2500', # ─
			vertical   = '\u2502', # │

			dash_h = '\u2504', # ┄
			dash_v = '\u2506', # ┆

			tiny_dash_h = '\u2508', # ┈
			tiny_dash_v = '\u250a', # ┊

			split_h      = '\u254c', # ╌
			left_half_h  = '\u2574', # ╴
			right_half_h = '\u2576', # ╶

			split_v       = '\u254e', # ╎
			top_half_v    = '\u2575', # ╵
			bottom_half_v = '\u2577', # ╷

			corner = DotDict(
				upper_left  = '\u250c', # ┌
				upper_right = '\u2510', # ┐
				lower_left  = '\u2514', # └
				lower_right = '\u2518', # ┘
			),
			rounded_corner = DotDict(
				upper_left  = '\u256d', # ╭
				upper_right = '\u256e', # ╮
				lower_left  = '\u2570', # ╰
				lower_right = '\u256f', # ╯
			),
			intersect = DotDict(
				T_LEFT   = '\u251c', # ├
				T_RIGHT  = '\u2524', # ┤
				T_TOP    = '\u252c', # ┬
				T_BOTTOM = '\u2534', # ┴
				CROSS    = '\u253c', # ┼
			),
		),
		bold = DotDict(
			horizontal = '\u2501', # ━
			vertical   = '\u2503', # ┃

			dash_h = '\u2505', # ┅
			dash_v = '\u2507', # ┇

			tiny_dash_h = '\u2509', #' ┉
			tiny_dash_v = '\u250b', #' ┋

			split_h      = '\u254d', #' ╍
			left_half_h  = '\u2578', #' ╸
			right_half_h = '\u257a', #' ╺

			split_v       = '\u254f', #' ╏
			top_half_v    = '\u2579', #' ╹
			bottom_half_v = '\u257b', #' ╻

			corner = DotDict(
				upper_left  = '\u250f', #' ┏
				upper_right = '\u2513', #' ┓
				lower_left  = '\u2517', #' ┗
				lower_right = '\u251b', #' ┛
			),
			intersect = DotDict(
				T_LEFT   = '\u2523', #' ┣
				T_RIGHT  = '\u252b', #' ┫
				T_TOP    = '\u2533', #' ┳
				T_BOTTOM = '\u253b', #' ┻
				CROSS    = '\u254b', #' ╋
			),
		),
		double = DotDict(
			horizontal = '\u2550', #' ═
			vertical   = '\u2551', #' ║

			corner = DotDict(
				upper_left  = '\u2554', #' ╔
				upper_right = '\u2557', #' ╗
				lower_left  = '\u255a', #' ╚
				lower_right = '\u255d', #' ╝
			),
			intersect = DotDict(
				T_LEFT   = '\u2560', #' ╠
				T_RIGHT  = '\u2563', #' ╣
				T_TOP    = '\u2566', #' ╦
				T_BOTTOM = '\u2569', #' ╩
				CROSS    = '\u256c', #' ╬
			),
		),
	)
	block = DotDict(

		shade_light = '\u2591', #' ░
		shade_med   = '\u2592', #' ▒
		shade_dark  = '\u2593', #' ▓

		v100 = '\u2588', #' █
		h100 = '\u2588', #' █
		full  = '\u2588', #' █

		v13 = '\u2581', #' ▁ (1/8 or 12.5%)
		v25 = '\u2582', #' ▂ (1/4 or 25%)
		v38 = '\u2583', #' ▃ (3/8 or 37.5%)
		v50 = '\u2584', #' ▄ (1/2 or 50%)
		v63 = '\u2585', #' ▅ (5/8 or 62.5%)
		v75 = '\u2586', #' ▆ (3/4 or 75%)
		v88 = '\u2587', #' ▇ (7/8 or 87.5%)

		h13 = '\u258f', #' ▏ (1/8 or 12.5%)
		h25 = '\u258e', #' ▎ (1/4 or 25%)
		h38 = '\u258d', #' ▍ (3/8 or 37.5%)
		h50 = '\u258c', #' ▌ (1/2 or 50%)
		h63 = '\u258b', #' ▋ (5/8 or 62.5%)
		h75 = '\u258a', #' ▊ (3/4 or 75%)
		h88 = '\u2589', #' ▉ (7/8 or 87.5%)

		v13_upper = '\u2594', #' ▔ (13% top-aligned)
		v50_upper = '\u2580', #' ▀ (50% top-aligned)

		h13_right = '\u2595', #' ▕ (13% right-aligned)
		h50_right = '\u2590', #' ▐ (50% right-aligned)

		#             1 | 2
		# Quadrants  ---+---
		#             3 | 4

		quad3   = '\u2596', #' ▖
		quad4   = '\u2597', #' ▗
		quad1   = '\u2598', #' ▘
		quad134 = '\u2599', #' ▙
		quad14  = '\u259a', #' ▚
		quad12  = '\u2580', #' ▀
		quad123 = '\u259b', #' ▛
		quad124 = '\u259c', #' ▜
		quad2   = '\u259d', #' ▝
		quad24  = '\u2590', #' ▐
		quad23  = '\u259e', #' ▞
		quad234 = '\u259f', #' ▟
		quad1234= '\u2588', #' █
		quad34  = '\u2584', #' ▄
		quad13  = '\u258c', #' ▌
	)
