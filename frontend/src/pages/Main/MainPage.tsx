import React from 'react';
import styles from './MainPage.module.scss';
import classNames from "classnames";
import Grid from '@material-ui/core/Grid';
import backgroundGreenGradient from '../../assets/images/background-green-gradient.png';
import { Icon, CircularProgress } from '@material-ui/core';

const MainPage = () => {
    const cx = classNames.bind(styles);

    return (
        <Grid className={cx(styles.container)} container
        >
            <Grid className={cx(styles.containerItem)} item xs={7}>
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
            }} className={cx(styles.containerItem)} item xs={5}>
                <div className={cx(styles.rightItemContainer)}>
                    <p className={cx(styles.itemTitle)}>
                        Сервис для идентификации по фотографии клиентов
                        банка и сбора их финансового профиля из различных открытых источников.
                    </p>
                    <Grid className={cx(styles.progressStepsContainer)} container alignItems="center">
                        <Grid item xs={2}>
                            <span className={cx(styles.progressStep)}>1</span>
                        </Grid>
                        <Grid item className={cx(styles.progressMessage)} xs={8}>
                            Добавьте ссылки
                        </Grid>
                       <Grid item xs={2}>
                           <span className={cx(styles.progressStep, styles.notActive)}>2</span>
                       </Grid>
                    </Grid>

                    {/*TODO: change text input after button clicked*/}
                    <textarea rows={12} className={cx(styles.textArea)}>
                    </textarea>
                    <button className={cx(styles.submitLinksButton)}>
                         ОТПРАВИТЬ
                    </button>

                    {/*TODO: upload Image*/}
                    {/*<div className={cx(styles.uploadImageButton)}>*/}
                    {/*    /!*<Icon>*!/*/}
                    {/*    /!*    backup*!/*/}
                    {/*    /!*</Icon>*!/*/}
                    {/*    */}
                    {/*    /!*TODO: add spinner when loading*!/*/}
                    {/*    <CircularProgress style={{color: 'white'}} size={50} />*/}
                    {/*</div>*/}
                    {/*<div className={cx(styles.infoBeforeUpdload)}>*/}

                    {/*</div>*/}
                </div>
            </Grid>
        </Grid>
    );
};

export { MainPage };
