<!-- Header Area -->
<header class="site-header site-header--menu-center site-header--absolute">
	<div class="container-fluid pr-lg-9 pl-lg-9">
		<nav class="px-0 navbar site-navbar offcanvas-active navbar-expand-lg">
			<!-- Brand Logo-->
			<div class="brand-logo">
				<a href="#" :to="/">
					<img
						src="https://ik.imagekit.io/codustry/gebwai/webapp/09122021/logo-text_E033c2W5g.svg?updatedAt=1631423536990"
						alt=""
						class="light-version-logo"
						height="40px"
					/>
					<!-- <lottie-player src="https://assets3.lottiefiles.com/packages/lf20_zymiw5rh.json"  background="transparent"  speed="1"  style="height: 50px;"  loop={true} autoplay={true}></lottie-player> -->
				</a>
			</div>
			<div class="collapse navbar-collapse" id="mobile-menu">
				<div class="navbar-nav-wrapper">
					<ul class="navbar-nav main-menu">
						<li class="nav-item dropdown">
							<a
								rel="prefetch"
								class="nav-link dropdown-toggle gr-toggle-arrow"
								id="navbarDropdown"
								href="#features"
								role="button"
								data-toggle="dropdown"
								aria-haspopup="true"
								aria-expanded="false">รู้จัก "เก็บไว้" <i class="icon icon-small-down" /></a
							>
							<ul class="gr-menu-dropdown dropdown-menu" aria-labelledby="navbarDropdown">
								<li class="drop-menu-item">
									<a href="#case">เก็บไว้ ช่วยอะไร?</a>
								</li>
								<li class="drop-menu-item">
									<a href="#start">เริ่มต้นใช้งาน</a>
								</li>
								<li class="drop-menu-item">
									<a href="#security">ความปลอดภัย</a>
								</li>
								<!-- <li class="drop-menu-item">
                            <a href="https://github.com/codustry/gebwai-community" target="_blank">คอมมูนิตี้</a>
                        </li>
                        <li class="drop-menu-item">
                            <a href="/privacy">นโยบายความเป็นส่วนตัว</a>
                        </li>
                        <li class="drop-menu-item">
                            <a href="https://m.me/gebwai" target="_blank">ติดต่อทีมงาน</a>
                        </li> -->
							</ul>
						</li>

						<li class="nav-item">
							<a class="nav-link" href="#pricing" role="button" aria-expanded="false">แพ็คเกจ</a>
						</li>

						<!-- <li class="nav-item">
                    <a rel="prefetch" class="nav-link" href="/blog" role="button" aria-expanded="false">บล็อก</a>
                </li> -->

						<li class="nav-item">
							<a
								rel="prefetch"
								class="nav-link"
								href="https://github.com/codustry/gebwai-community"
								target="_blank"
								role="button"
								aria-expanded="false">คอมมูนิตี้</a
							>
						</li>

						<li class="nav-item dropdown">
							<a
								class="nav-link dropdown-toggle gr-toggle-arrow"
								id="navbarDropdown"
								href="#features"
								role="button"
								data-toggle="dropdown"
								aria-haspopup="true"
								aria-expanded="false">ความช่วยเหลือ <i class="icon icon-small-down" /></a
							>
							<ul class="gr-menu-dropdown dropdown-menu" aria-labelledby="navbarDropdown">
								<li class="drop-menu-item">
									<a rel="prefetch" href="/faq">คำถามที่พบบ่อย</a>
								</li>
								<!-- <li class="drop-menu-item">
                            <a href="https://github.com/codustry/gebwai-community" target="_blank">คอมมูนิตี้</a>
                        </li> -->
								<li class="drop-menu-item">
									<a rel="prefetch" href="/privacy">นโยบายความเป็นส่วนตัว</a>
								</li>
								<li class="drop-menu-item">
									<a rel="prefetch" href="https://lin.ee/V0hvk0D" target="_blank">ติดต่อทีมงาน</a>
								</li>
							</ul>
						</li>
					</ul>
				</div>
				<button
					class="d-block d-lg-none offcanvas-btn-close"
					type="button"
					data-toggle="collapse"
					data-target="#mobile-menu"
					aria-controls="mobile-menu"
					aria-expanded="true"
					aria-label="Toggle navigation"
				>
					<i class="gr-cross-icon" />
				</button>
			</div>
			<div class="ml-auto mr-6 header-btn ml-lg-0 mr-lg-0 d-none d-xs-block">
				<a rel="prefetch" class="btn btn-line" href="https://lin.ee/BJ4dbWO" target="_blank">
					<img
						src="https://ik.imagekit.io/codustry/gebwai/webapp/09122021/icon-line_0rpRKefoO.svg?updatedAt=1631423624423"
						height="20px"
						style="padding-right: 10px;"
					/> เพิ่มเพื่อน
				</a>
			</div>
			<!-- Mobile Menu Hamburger-->
			<button
				class="border-0 navbar-toggler btn-close-off-canvas hamburger-icon"
				type="button"
				data-toggle="collapse"
				data-target="#mobile-menu"
				aria-controls="mobile-menu"
				aria-expanded="false"
				aria-label="Toggle navigation"
			>
				<!-- <i class="icon icon-simple-remove icon-close"></i> -->
				<span class="hamburger hamburger--squeeze js-hamburger">
					<span class="hamburger-box">
						<span class="hamburger-inner" />
					</span>
				</span>
			</button>
			<!--/.Mobile Menu Hamburger Ends-->
		</nav>
	</div>
</header>
