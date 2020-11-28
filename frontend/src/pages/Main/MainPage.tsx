import React from 'react';
import styles from './MainPage.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';
import backgroundGreenGradient from '../../assets/images/background-green-gradient.png';

const MainPage = () => {
    const cx = classNames.bind(styles);

    return (
        <Grid className={cx(styles.container)} container
        >
            <Grid className={cx(styles.containerItem)} item sm={6}>
                <div className={cx(styles.leftItemContainer)}>
                    <div>
                        <h1>Invenient<br/> Face</h1>
                        <p>INNOTECH HACK</p>
                    </div>
                </div>
            </Grid>
            <Grid style={{
                background: `url(${backgroundGreenGradient})`,
                backgroundPosition: 'center',
                backgroundSize: 'cover'
            }} className={cx(styles.containerItem)} item sm={6}>
                <div className={cx(styles.rightItemContainer)}>
                    <p className={cx(styles.rightItemTitle)}>
                        Сервис для идентификации по фотографии клиентов
                        банка и сбора их финансового профиля из различных открытых источников.
                    </p>
                    <Grid className={cx(styles.progressStepsContainer)} container alignItems="center">
                        <Grid xs={2}>
                            <span className={cx(styles.progressStep)}>1</span>
                        </Grid>
                        <Grid className={cx(styles.progressMessage)} xs={8}>
                            Добавьте ссылки
                        </Grid>
                       <Grid xs={2}>
                           <span className={cx(styles.progressStep, styles.notActive)}>2</span>
                       </Grid>
                    </Grid>
                    <textarea rows={12} className={cx(styles.textArea)}>

                    </textarea>
                    <div className={cx(styles.infoBeforeUpdload)}>

                    </div>
                </div>
            </Grid>
        </Grid>
    );
};

export { MainPage };
